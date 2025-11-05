import requests, json, os, sys, time, threading, random

C = {
    "cyan": "\033[1;36m",
    "blue": "\033[1;34m",
    "green": "\033[1;32m",
    "magenta": "\033[1;35m",
    "yellow": "\033[1;33m",
    "red": "\033[1;31m",
    "white": "\033[1;37m",
    "reset": "\033[0m"
}


banner = f"""
{C['blue']}╔═════════════════════════════════════════════════════════════════╗
{C['green']}║ ██╗  ██╗██████╗ ████████╗  ████████╗ ██████╗  ██████╗ ██╗       ║
{C['magenta']}║ ██║  ██║██╔══██╗╚══██╔══╝  ╚══██╔══╝██╔═══██╗██╔═══██╗██║       ║
{C['red']}║ ███████║██║  ██║   ██║ █████╗ ██║   ██║   ██║██║   ██║██║       ║
{C['yellow']}║ ██╔══██║██║  ██║   ██║ ╚════╝ ██║   ██║   ██║██║   ██║██║       ║
{C['blue']}║ ██║  ██║██████╔╝   ██║        ██║   ╚██████╔╝╚██████╔╝███████╗  ║
{C['white']}║ ╚═╝  ╚═╝╚═════╝    ╚═╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝  ║
{C['blue']}╠═════════════════════════════════════════════════════════════════╣
{C['green']}║➢ Author   : APIDev-AI                                            ║
{C['cyan']}║➢ Youtube  : https://youtube.com/@APIDev-AI                        ║
{C['red']}║➢ Zalo     : https://zalo.me/g/pxwhiq299                          ║
{C['yellow']}║➢ Website  : https://apidev-ai.blogspot.com                       ║
{C['blue']}╚═════════════════════════════════════════════════════════════════╝
{C['reset']}
"""

API_KEY = "AIzaSyAC2BF_kdo0TuLHXUtYsxVqa67F3IaSyvk"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

def type_effect(text, delay=0.002):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spinner(text):
    stop_flag = threading.Event()
    lock = threading.Lock()

    def spin():
        frames = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
        i = 0
        while not stop_flag.is_set():
            frame = frames[i % len(frames)]
            with lock:
                sys.stdout.write(f"\r{C['cyan']}{text} {frame}{C['reset']}")
                sys.stdout.flush()
            time.sleep(0.1)
            i += 1
        
        with lock:
            sys.stdout.write("\r" + " " * (len(text) + 6) + "\r")
            sys.stdout.flush()

    thread = threading.Thread(target=spin)
    thread.daemon = True
    thread.start()
    return stop_flag, lock

def ask_apidev(prompt):
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    try:
        res = requests.post(URL, headers=headers, data=json.dumps(payload))
        if res.status_code == 200:
            data = res.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"⚠️ Lỗi HTTP {res.status_code}: {res.text}"
    except Exception as e:
        return f"❌ Lỗi: {e}"

def chat_loop():
    while True:
        user = input(f"{C['cyan']}APIDev-AI › {C['reset']}").strip()
        if user.lower() in ["exit", "quit"]:
            print(f"{C['magenta']}Tạm biệt!{C['reset']}")
            break
        if not user:
            continue

        stop_flag, lock = spinner("[APIDevAI] APIDev-AI đang suy nghĩ")
        answer = ask_apidev(user)
        stop_flag.set()
        time.sleep(0.1)

        with lock:
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()

        print(f"{C['blue']}[APIDevAI] APIDev-AI:{C['reset']} ", end="")
        type_effect(answer, 0.0016)
        print()

def loading():
    os.system("cls" if os.name == "nt" else "clear")
    print(banner)
    print(f"{C['cyan']}Đang khởi tạo hệ thống APIDev-AI...{C['reset']}\n")
    bar = ""
    for i in range(40):
        bar += random.choice(["█", "▓", "▒", "░"])
        sys.stdout.write(f"\r{C['green']}[{bar:<40}] {int((i+1)/40*100)}%{C['reset']}")
        sys.stdout.flush()
        time.sleep(0.05)
    print(f"\n\n{C['green']}✅ Hệ thống đã sẵn sàng!{C['reset']}")
    time.sleep(0.6)
    os.system("cls" if os.name == "nt" else "clear")
    print(banner)
    print(f"{C['white']}Gõ '{C['cyan']}exit{C['white']}' để thoát.\n{C['reset']}")

if __name__ == "__main__":
    loading()
    chat_loop()
