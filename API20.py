    try:
        os.chdir("BotZalo")

        os.system("python3 main.py")

    except Exception as e:
        print(f"Lỗi: {e}")
