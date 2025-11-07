import os, sys, time, datetime
import pyautogui

try:
    import pyperclip
    HAS_PYPERCLIP = True
except Exception:
    HAS_PYPERCLIP = False

GROUP_NAME = "SE-AI-B3-1"
BASE_MESSAGE = "One week completed"
INCLUDE_DATE = True
DRY_RUN = False

APP_BOOT_WAIT = 8
SEARCH_WAIT = 0.8
OPEN_CHAT_WAIT = 0.8
TYPE_INTERVAL = 0.02

def paste_text(txt):
    if HAS_PYPERCLIP:
        import pyperclip
        pyperclip.copy(txt)
        pyautogui.hotkey("ctrl", "v")
    else:
        pyautogui.typewrite(txt, interval=TYPE_INTERVAL)

def build_message():
    msg = BASE_MESSAGE
    if INCLUDE_DATE:
        msg += " — " + datetime.datetime.now().strftime("%d-%b-%Y")
    return msg

def focus_chat():
    # open search
    pyautogui.hotkey("ctrl", "f")
    time.sleep(SEARCH_WAIT)
    pyautogui.hotkey("ctrl", "a")
    pyautogui.press("backspace")
    paste_text(GROUP_NAME)
    time.sleep(0.8)
    pyautogui.press("down")
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(OPEN_CHAT_WAIT)

def click_message_box():
    """Click in the bottom-right chat input area."""
    w, h = pyautogui.size()
    # 90% width, 92% height → near bottom-right corner where message box is
    pyautogui.click(int(w * 0.9), int(h * 0.92))
    time.sleep(0.3)

def main():
    pyautogui.FAILSAFE = True

    print("Bringing up WhatsApp window...")
    os.startfile("whatsapp:")
    time.sleep(APP_BOOT_WAIT)

    print("Searching for group...")
    focus_chat()

    print("Clicking message box...")
    click_message_box()

    msg = build_message()
    print(f"Typing: {msg}")
    paste_text(msg)

    if not DRY_RUN:
        pyautogui.press("enter")
        print(f"✅ Message sent to {GROUP_NAME}")
    else:
        print("[DRY_RUN] Message composed but not sent.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
