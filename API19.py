import smtplib
import time
import os
import sys
import socket
import requests
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ===== MÀU SẮC =====
den = "\033[1;30m"
xanhla = "\033[1;92m"
do_nhat = "\033[1;91m"
vang_nhat = "\033[1;93m"
xanhduong_sang = "\033[1;94m"
hong_nhat = "\033[1;95m"
trang_sang = "\033[1;97m"
xnhac = "\033[1;36m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xanhd = "\033[1;34m"
hong = "\033[1;35m"
trang = "\033[1;37m"
reset = "\033[0m"

EMAIL = "llolgarena@gmail.com"
PASSWORD = "ucjpcwxujmxzlwqw"


def get_ip():
    try:
        url = "http://kiemtraip.com/raw.php"
        ip = socket.gethostbyname(requests.get(url).text.strip())
        return ip
    except:
        return "Không xác định"


now = datetime.now()
ngay = now.strftime("%d")
thang = now.strftime("%m")
nam = now.strftime("%Y")
ip = get_ip()


def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"""{xanhd}╔═════════════════════════════════════════════════════════════════╗
{luc}║  █████╗ ██████╗ ██╗██████╗ ███████╗██╗   ██╗                   ║
{hong}║ ██╔══██╗██╔══██╗██║██╔══██╗██╔════╝╚██╗ ██╔╝                   ║
{do}║ ███████║██████╔╝██║██║  ██║█████╗   ╚████╔╝                    ║
{vang}║ ██╔══██║██╔═══╝ ██║██║  ██║██╔══╝    ╚██╔╝                     ║
{xanhd}║ ██║  ██║██║     ██║██████╔╝███████╗   ██║                      ║
{trang}║ ╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚══════╝   ╚═╝                      ║
{xanhd}╠═════════════════════════════════════════════════════════════════╣
{luc}║➢ Author   : APIEmail Tool                                        ║
{xnhac}║➢ Youtube  : https://youtube.com/@APIDev-ThienNhan               ║
{do}║➣ Nhóm Zalo: https://zalo.me/g/pxwhiq299                         ║
{vang}║➣ Website  : https://devthiennhan.bio.link                       ║
{hong}║➣ IP Hiện Tại: {vang}{ip:<43}{trang}║
{xnhac}║➣ Ngày: {do}{ngay}{vang} | {luc}Tháng: {do}{thang}{vang} | {luc}Năm: {do}{nam}{vang}{" " * 17}║
{xanhd}╚═════════════════════════════════════════════════════════════════╝{reset}
""")


def loading(text, duration=2):
    animation = ["|", "/", "-", "\\"]
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f"\r{xanhduong_sang}{text} {vang}{animation[i % len(animation)]}{reset}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * (len(text) + 5) + "\r")


def progress_bar(current, total, bar_length=30):
    percent = current / total
    filled = int(bar_length * percent)
    bar = f"{xanhla}{'█' * filled}{reset}{den}{'░' * (bar_length - filled)}"
    sys.stdout.write(f"\r{trang}Tiến trình: [{bar}] {vang}{percent * 100:.1f}%{reset}")
    sys.stdout.flush()
    if current == total:
        print()


def send_email(to_email, subject, message):
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL, PASSWORD)
        server.sendmail(EMAIL, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        return str(e)


def ask(prompt, default=None, multi=False, limit=None):
    mau_list = [xanhduong_sang, xnhac, luc, hong_nhat, vang]
    mau_prompt = mau_list[hash(prompt) % len(mau_list)]
    print(f"{mau_prompt}➤ {trang_sang}{prompt}{reset}")
    print(f"{xanhduong_sang}> {reset}", end="")

    if multi:
        values = []
        while True:
            val = input().strip()
            if val == "":
                break
            values.append(val)
            if limit and len(values) >= limit:
                break
            print(f"{mau_prompt}> {reset}", end="")
        return values
    else:
        val = input().strip()
        return val or default


def apiemail_run():
    banner()

    subject = ask("Nhập tiêu đề thư", "Thư tự động từ APIEmail")
    noidungs = ask("Nhập nội dung thư (Enter trống để kết thúc)", multi=True, limit=10)
    if not noidungs:
        print(f"{do_nhat}Không có nội dung nào được nhập.{reset}")
        sys.exit()

    solan = int(ask("Nhập số lần gửi"))
    delay = float(ask("Nhập thời gian chờ giữa các lần gửi (giây)"))

    email_nhan = ask("Nhập email nhận (Enter trống để kết thúc)", multi=True, limit=10)
    if not email_nhan:
        print(f"{do_nhat}Chưa nhập email nhận nào!{reset}")
        sys.exit()

    total = solan * len(email_nhan)
    print(f"\n{luc}Bắt đầu gửi {total} email...{reset}\n")

    success, fail = [], []
    count = 0

    for i in range(solan):
        for mail in email_nhan:
            content = noidungs[i % len(noidungs)]
            loading(f"Đang gửi tới {mail}", 1.0)
            result = send_email(mail, subject, content)
            count += 1
            progress_bar(count, total)
            if result is True:
                success.append(mail)
            else:
                fail.append((mail, result))
            time.sleep(delay)

    print(f"\n{trang_sang}╔══════════════════════════════════════╗{reset}")
    print(f"{trang_sang}║         {xanhduong_sang}BẢNG KẾT QUẢ GỬI MAIL{trang_sang}         ║{reset}")
    print(f"{trang_sang}╚══════════════════════════════════════╝{reset}")

    for mail in success:
        print(f"{luc}[✓] {trang}Đã gửi tới: {xanhduong_sang}{mail}{reset}")
    for mail, err in fail:
        print(f"{do}[X] {trang}Lỗi gửi tới: {do_nhat}{mail} → {vang_nhat}{err}{reset}")

    print(f"\n{vang_nhat}Tổng cộng: {trang}{len(success)} thành công, {do}{len(fail)} thất bại.{reset}\n")


if __name__ == "__main__":
    apiemail_run()
