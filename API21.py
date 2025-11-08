with lock:
  sys.stdout.write("\r" + " " * (len(text) + 6) + "\r")
sys.stdout.flush()

thread = threading.Thread(target = spin)
thread.daemon = True
thread.start()
return stop_flag, lock

def ask_apidev(prompt):
  payload = {
    "contents": [{
      "parts": [{
        "text": prompt
      }]
    }]
  }
headers = {
  "Content-Type": "application/json"
}
try:
res = requests.post(URL, headers = headers, data = json.dumps(payload))
if res.status_code == 200:
  data = res.json()
return data["candidates"][0]["content"]["parts"][0]["text"]
else:
  return f "⚠️ Lỗi HTTP {res.status_code}: {res.text}"
except Exception as e:
  return f "❌ Lỗi: {e}"

def chat_loop():
  while True:
  user = input(f "{C['cyan']}APIDev-AI › {C['reset']}").strip()
if user.lower() in ["exit", "quit"]:
  print(f "{C['magenta']}Tạm biệt!{C['reset']}")
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

print(f "{C['blue']}[APIDevAI] APIDev-AI:{C['reset']} ", end = "")
type_effect(answer, 0.0016)
print()

def loading():
  os.system("cls"
    if os.name == "nt"
    else "clear")
print(banner)
print(f "{C['cyan']}Đang khởi tạo hệ thống APIDev-AI...{C['reset']}\n")
bar = ""
for i in range(40):
  bar += random.choice(["█", "▓", "▒", "░"])
sys.stdout.write(f "\r{C['green']}[{bar:<40}] {int((i+1)/40*100)}%{C['reset']}")
sys.stdout.flush()
time.sleep(0.05)
print(f "\n\n{C['green']}✅ Hệ thống đã sẵn sàng!{C['reset']}")
time.sleep(0.6)
os.system("cls"
  if os.name == "nt"
  else "clear")
print(banner)
print(f "{C['white']}Gõ '{C['cyan']}exit{C['white']}' để thoát.\n{C['reset']}")

if __name__ == "__main__":
  loading()
chat_loop()
