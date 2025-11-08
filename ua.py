import requests
import os

# Định nghĩa màu sắc cho đầu ra
den = "\033[1;30m"
do = "\033[1;31m"
luc = "\033[1;32m"
vang = "\033[1;33m"
xanhd = "\033[1;34m"
hong = "\033[1;35m"
xnhac = "\033[1;36m"
trang = "\033[1;37m"
whiteb = "\033[1;37m"
red = "\033[0;31m"
redb = "\033[1;31m"
end = '\033[0m'
xanhla = "\033[1;92m"
do_nhat = "\033[1;91m"
vang_nhat = "\033[1;93m"
xanhduong_sang = "\033[1;94m"
hong_nhat = "\033[1;95m"
trang_sang = "\033[1;97m"
den = "\033[1;90m"
luc = "\033[1;32m"
trang = "\033[1;37m"
red = "\033[1;31m"
vang = "\033[1;33m"
tim = "\033[1;35m"
lamd = "\033[1;34m"
lam = "\033[1;36m"
purple = "\033[35m"
hong = "\033[1;95m"
trang = "\033[1;37m\033[1m"
xanh_la = "\033[1;32m\033[1m"
vang = "\033[1;33m\033[1m"
reset = "\033[0m"

hack = "\033[1;31m[\033[1;37m😜\033[1;31m] \033[1;37m=> "
banner = f"""
\033[1;32m║  █████╗ ██████╗ ██╗██████╗ ███████╗██╗   ██╗                   ║
\033[1;35m║ ██╔══██╗██╔══██╗██║██╔══██╗██╔════╝╚██╗ ██╔╝                   ║
\033[1;31m║ ███████║██████╔╝██║██║  ██║█████╗   ╚████╔╝                    ║
\033[1;33m║ ██╔══██║██╔═══╝ ██║██║  ██║██╔══╝    ╚██╔╝                     ║
\033[1;34m║ ██║  ██║██║     ██║██████╔╝███████╗   ██║                      ║
\033[1;37m║ ╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚══════╝   ╚═╝                      ║
\033[1;34m╠═════════════════════════════════════════════════════════════════╣
 
BOX ZALO: https://zalo.me/g/pxwhiq299
ADMIN : APIDev
YTB : APIDevThienNhan
\033[1;97m= = = = = = = = = = = = = = = = = = = = = = = = = = = = = """
os.system('cls' if os.name == 'nt' else 'clear')
print(banner)

def shorten_link(url):
    token = "6908b37569ea03733d2ed6c9"
    api_url = f"https://link4m.co/api-shorten/v2?api={token}&url={url}"

    response = requests.get(api_url)

    if response.status_code == 200:
        return response.text  # Dữ liệu trả về là dạng text
    else:
        return "Error: " + str(response.status_code) + " - " + response.text

# Sử dụng tool
link = input(f"{hack}NHẬP LINK CẦN RÚT GỌN : {vang}")

# Rút gọn URL với API link4m.co
token_link1s = '6908b37569ea03733d2ed6c9'
response = requests.get(f'https://link4m.co/api-shorten/v2?api={token_link1s}&url={link}').json()

if response.get('status') == "error":
    print(f"Lỗi: {response.get('message')}")
else:
    shortened_link = response.get('shortenedUrl')
    print(f"{hack}{xanh_la}LINK RÚT GỌN CỦA BẠN LÀ: {vang}{shortened_link}")