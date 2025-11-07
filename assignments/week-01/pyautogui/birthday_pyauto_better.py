import json
import os
import time
import webbrowser
from datetime import datetime, date
from typing import List, Dict, Optional
from urllib.parse import quote_plus

import pyautogui

# Optional clipboard paste (more reliable than typing). Falls back gracefully.
try:
    import pyperclip
    HAS_PYPERCLIP = True
except Exception:
    HAS_PYPERCLIP = False

# ========== CONFIG ==========
USE_GMAIL = True       # True = Gmail compose URL, False = mailto: (Outlook desktop / default client)
DRY_RUN = False        # True = preview only (won't press Ctrl+Enter)
OPEN_WAIT = 4          # seconds to wait after opening compose (baseline; retries will add more)
MAX_RETRIES = 3        # how many times to wait-and-retry before giving up
BETWEEN_EMAILS = 2     # small gap between recipients
SUBJECT = "Happy Birthday! 🎉"
BODY_TEMPLATE = (
    "Hi,\n\nWishing you a very happy birthday! 🎂🎈\n"
    "Have a fantastic year ahead.\n\nWarm regards,\nYour Team"
)
SENT_LOG = "sent_log.json"  # stores emails sent per day to avoid duplicates

# Example data (replace with your source)
people: List[Dict[str, str]] = [
    {"email": "chrismckadi@gmail.com", "date": "2000-11-07"},
    {"email": "mcenroedavidmascurenas@gmail.com",  "date": "07-11"},   # DD-MM
    {"email": "li@example.com",   "date": "11/07"},   # MM/DD
    # {"email": "leap@example.com", "date": "2004-02-29"},  # test leap birthday
]

# ========== DATE HELPERS ==========
def parse_month_day(s: str) -> Optional[tuple]:
    """Accept many formats; return (month, day) or None."""
    s = s.strip()
    fmts = [
        "%Y-%m-%d", "%d-%m-%Y", "%m-%d-%Y",
        "%d-%m", "%m-%d",
        "%d/%m/%Y", "%m/%d/%Y",
        "%d/%m", "%m/%d",
    ]
    from datetime import datetime as dt
    for f in fmts:
        try:
            d = dt.strptime(s, f)
            return (d.month, d.day)
        except ValueError:
            pass
    return None

def is_leap_year(y: int) -> bool:
    return (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)

def is_birthday_today(date_str: str) -> bool:
    md = parse_month_day(date_str)
    if not md:
        return False
    m, d = md
    today = date.today()
    # Optional: map 29-Feb birthdays to 28-Feb in non-leap years
    if (m, d) == (2, 29) and not is_leap_year(today.year):
        return (today.month, today.day) == (2, 28)
    return (today.month, today.day) == (m, d)

# ========== URL BUILDERS ==========
def gmail_compose_url(to_email: str, subject: str, body: str) -> str:
    base = "https://mail.google.com/mail/?view=cm&fs=1&tf=1"
    return f"{base}&to={quote_plus(to_email)}&su={quote_plus(subject)}&body={quote_plus(body)}"

def mailto_url(to_email: str, subject: str, body: str) -> str:
    return f"mailto:{to_email}?subject={quote_plus(subject)}&body={quote_plus(body)}"

def open_compose(to_email: str, subject: str, body: str):
    url = gmail_compose_url(to_email, subject, body) if USE_GMAIL else mailto_url(to_email, subject, body)
    webbrowser.open_new_tab(url)

# ========== SENT LOG ==========
def load_sent_log() -> dict:
    if not os.path.exists(SENT_LOG):
        return {}
    try:
        with open(SENT_LOG, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_sent_log(log: dict):
    with open(SENT_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2)

def already_sent_today(email: str, log: dict) -> bool:
    today_key = date.today().isoformat()
    return email.lower() in set(map(str.lower, log.get(today_key, [])))

def mark_sent_today(email: str, log: dict):
    today_key = date.today().isoformat()
    log.setdefault(today_key, [])
    if email not in log[today_key]:
        log[today_key].append(email)
    save_sent_log(log)

# ========== ACTIONS ==========
def press_send():
    if DRY_RUN:
        print(" [DRY_RUN] Would press Ctrl+Enter")
        return
    pyautogui.hotkey("ctrl", "enter")

def wait_compose_ready():
    # Simple retry loop; if your network is slow, this is safer than a single sleep.
    delay = OPEN_WAIT
    for attempt in range(1, MAX_RETRIES + 1):
        time.sleep(delay)
        # Heuristic: send a harmless Tab to ensure focus is in the window
        pyautogui.press("tab")
        # If you want to be extra sure, you could try image detection for a "Send" button here.
        # (Requires a reference image and consistent UI theme.)
        return True
        # If you actually add image detection, break only when found; otherwise increase delay and retry.
        # delay += 2
    return True

def paste_or_type(text: str):
    # If using mailto (Outlook desktop), you might want to paste the body manually
    if HAS_PYPERCLIP:
        pyperclip.copy(text)
        pyautogui.hotkey("ctrl", "v")
    else:
        pyautogui.typewrite(text, interval=0.02)

# ========== MAIN ==========
def main():
    pyautogui.FAILSAFE = True
    log = load_sent_log()

    todays = [p for p in people if p.get("email") and p.get("date") and is_birthday_today(p["date"])]
    if not todays:
        print("ℹ️ No birthdays today.")
        return

    print(f"🎂 Found {len(todays)} birthday(s) today.")
    for idx, p in enumerate(todays, 1):
        email = p["email"].strip()
        if already_sent_today(email, log):
            print(f" • Skipping (already sent): {email}")
            continue

        # If you want to personalize: add "name" to dicts and do:
        body = BODY_TEMPLATE  # or f"Hi {p.get('name','')},\n\n..."

        print(f"\n[{idx}/{len(todays)}] Opening compose for: {email}")
        open_compose(email, SUBJECT, body)

        # If using mailto (Outlook desktop), the subject/body may not always prefill reliably.
        # In that case, uncomment below to force-fill via clipboard:
        # if not USE_GMAIL:
        #     time.sleep(2)
        #     # Focus Subject (Outlook desktop: Alt+S won't go to subject; better to send Tabs or click once manually)
        #     # Here we assume caret is in To: line → press Tab to Subject, paste, then Tab to body:
        #     pyautogui.press("tab")
        #     if HAS_PYPERCLIP:
        #         pyperclip.copy(SUBJECT); pyautogui.hotkey("ctrl", "v")
        #     else:
        #         pyautogui.typewrite(SUBJECT, interval=0.02)
        #     pyautogui.press("tab")
        #     paste_or_type(body)

        wait_compose_ready()
        print(" → Sending (Ctrl+Enter)…")
        press_send()
        print(" ✓ Sent trigger fired.")

        mark_sent_today(email, log)
        time.sleep(BETWEEN_EMAILS)

    print("\n✅ All done.")

if __name__ == "__main__":
    main()
