import re
import json
import asyncio
import argparse
from pathlib import Path
from urllib.parse import urlparse, urlunparse
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

URL = "https://www.cricbuzz.com/live-cricket-scorecard/121681/indw-vs-rsaw-final-icc-womens-world-cup-2025"
XPATH_ROOT = "/html/body/div/main/div/div[2]/div[1]/div/div"  # your root that contains the whole scorecard
OUT_JSON = Path("scorecard.json")

def clean(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

def force_www(u: str) -> str:
    p = urlparse(u)
    host = p.netloc.replace("m.cricbuzz.com", "www.cricbuzz.com").replace("amp.cricbuzz.com", "www.cricbuzz.com")
    return urlunparse(p._replace(netloc=host))

def is_number(x: str) -> bool:
    return bool(re.match(r"^\d+(\.\d+)?$", x))

async def wait_scorecard_root(page):
    root = page.locator(f"xpath={XPATH_ROOT}")
    await root.wait_for(state="visible", timeout=15000)
    return root

async def get_innings_blocks(root):
    # Cricbuzz innings usually live under ids like scard-team-<id>-innings-<n>
    inns = root.locator('[id^="scard-team-"][id*="innings"]')
    if await inns.count() == 0:
        # fallback: some pages wrap innings differently; use large blocks that contain batting rows
        inns = root.locator("div:has(.cb-scrd-itms)")
    return inns

async def extract_header_text(block):
    # Try common header holders
    for sel in [".cb-scrd-hdr-rw", "h2", "h3", "div:has-text('Innings')"]:
        loc = block.locator(sel)
        if await loc.count():
            txt = clean(await loc.first.inner_text())
            if txt:
                return txt
    # fallback to first line of the block
    return clean(await block.first.inner_text())[:80] or "Innings"

async def parse_batting_and_bowling(block):
    """
    Distinguish batting vs bowling using tail patterns:
      Batting tail: R, B, 4s, 6s, SR (5 numbers, last is decimal SR)
      Bowling tail: O, M, R, W, NB, WD, ECO (7 numbers, first+last can be decimal)
    Also capture 'Extras' & 'Total' lines and 'Fall of Wickets'.
    """
    batting, bowling = [], []
    extras, total, fow = None, None, None

    rows = block.locator(".cb-scrd-itms")
    rc = await rows.count()

    for i in range(rc):
        r = rows.nth(i)
        cells = [clean(x) for x in await r.locator("div, span, td, th").all_inner_texts()]
        cells = [c for c in cells if c]
        if not cells:
            continue
        joined = " ".join(cells)

        # Try to catch Extras / Total / FoW lines early
        if re.search(r"^\s*Extras\s*:", joined, re.I):
            extras = clean(joined)
            continue
        if re.search(r"^\s*Total\s*", joined, re.I):
            total = clean(joined)
            continue
        if re.search(r"Fall of wickets|Fall of Wickets|FOW", joined, re.I):
            fow = clean(joined)
            continue

        # Identify batting rows: last 5 = R B 4s 6s SR
        if len(cells) >= 6:
            tail5 = cells[-5:]
            if all(re.match(r"^[\d-]+(\.\d+)?$", x) for x in tail5[:-1]) and re.match(r"^[\d\.]+$", tail5[-1]):
                name = " ".join(cells[:-5])
                # filter non-player lines
                if not re.search(r"(extras|total|did not bat)", name, re.I):
                    batting.append({
                        "batsman": name,
                        "R": tail5[0], "B": tail5[1], "4s": tail5[2], "6s": tail5[3], "SR": tail5[4],
                    })
                    continue

        # Identify bowling rows: last 7 = O M R W NB WD ECO
        if len(cells) >= 7:
            tail7 = cells[-7:]
            # first and last are typically decimals (O/ECO)
            if is_number(tail7[0]) and is_number(tail7[-1]) and all(is_number(x) for x in tail7[1:-1]):
                name = " ".join(cells[:-7]) or cells[0]
                if not re.match(r"^\d", name):  # name shouldn’t start numeric
                    bowling.append({
                        "bowler": name,
                        "O": tail7[0], "M": tail7[1], "R": tail7[2], "W": tail7[3],
                        "NB": tail7[4], "WD": tail7[5], "ECO": tail7[6],
                    })
                    continue

    # Secondary pass: if Extras/Total not captured, look for explicit labels near the end of block
    if extras is None:
        try:
            ex = block.locator("text=/^\\s*Extras/i").first
            if await ex.count():
                extras = clean(await ex.inner_text())
        except Exception:
            pass
    if total is None:
        try:
            tot = block.locator("text=/^\\s*Total/i").first
            if await tot.count():
                total = clean(await tot.inner_text())
        except Exception:
            pass

    # FoW sometimes outside rows
    if fow is None:
        try:
            fow_el = block.locator("text=/Fall of wickets|Fall of Wickets|FOW/i").first
            if await fow_el.count():
                # include its parent text (often the wickets list follows)
                container = fow_el.locator("xpath=ancestor::*[self::div or self::section][1]")
                fow = clean(await container.first.inner_text())
        except Exception:
            pass

    return batting, bowling, extras, total, fow

def print_innings(inn):
    print(f"\n=== {inn['header']} ===")
    if inn.get("batting"):
        print("\nBATTING")
        print(f"{'Batsman':35}  R   B  4s  6s   SR")
        for r in inn["batting"]:
            print(f"{r['batsman'][:35]:35}  {r['R']:>3} {r['B']:>3} {r['4s']:>3} {r['6s']:>3} {r['SR']:>6}")
    else:
        print("\nBATTING: (none)")

    if inn.get("extras"):
        print("Extras:", inn["extras"])
    if inn.get("total"):
        print("Total :", inn["total"])

    if inn.get("bowling"):
        print("\nBOWLING")
        print(f"{'Bowler':35}  O    M    R    W   NB  WD   ECO")
        for r in inn["bowling"]:
            print(f"{r['bowler'][:35]:35}  {r['O']:>4} {r['M']:>4} {r['R']:>4} {r['W']:>3} {r['NB']:>3} {r['WD']:>3} {r['ECO']:>5}")
    else:
        print("\nBOWLING: (none)")

    if inn.get("fow"):
        print("\nFOW:", inn["fow"])

async def main(headless: bool):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=headless, args=["--start-maximized"])
        ctx = await browser.new_context(viewport={"width": 1366, "height": 900})
        page = await ctx.new_page()

        await page.goto(force_www(URL), wait_until="domcontentloaded")

        # 1) scope to your XPath root (entire scorecard area)
        root = await wait_scorecard_root(page)

        # 2) find innings containers within that root
        innings_blocks = await get_innings_blocks(root)
        count = await innings_blocks.count()
        if count == 0:
            raise RuntimeError("Could not locate innings blocks inside the given XPath root.")

        all_innings = []
        for i in range(count):
            blk = innings_blocks.nth(i)
            header = await extract_header_text(blk)
            batting, bowling, extras, total, fow = await parse_batting_and_bowling(blk)
            all_innings.append({
                "header": header,
                "batting": batting,
                "extras": extras,
                "total": total,
                "bowling": bowling,
                "fow": fow,
            })

        # 3) print & save
        print("URL:", page.url)
        for inn in all_innings:
            print_innings(inn)

        with OUT_JSON.open("w", encoding="utf-8") as f:
            json.dump({"url": page.url, "innings": all_innings}, f, indent=2, ensure_ascii=False)
        print(f"\nSaved: {OUT_JSON.resolve()}")

        await ctx.close()
        await browser.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Cricbuzz whole scorecard (scoped to your XPath root)")
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()
    asyncio.run(main(args.headless))
