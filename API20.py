try:
    os.chdir("GayBotNhan")
    os.system("python3 Api.py")
except Exception as e:
    print(f"Lỗi: {e}")
