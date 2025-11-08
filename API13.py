import os
import sys
import subprocess
import time
import json
import random
import platform
import re
import math
import uuid
import base64
import socket
import hashlib
import threading
import ast
import ssl

import requests
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from time import sleep, strftime
from urllib.parse import urlencode
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar
from pathlib import Path
from pystyle import Write, Colors

now = datetime.now()
time_str = now.strftime("%H:%M:%S")
today = date.today()
thu = now.strftime("%A")
ngay_hom_nay = now.strftime("%d")
thang_nay = now.strftime("%m")
nam_ = now.strftime("%Y")

def get_ip_from_url(url):
    try:
        response = requests.get(url, timeout=5)
        if response.ok:
            host = response.text.strip()
            ip_address = socket.gethostbyname(host)
            return ip_address
        else:
            return "Không xác định"
    except Exception:
        return "Không xác định"

url_check = "http://kiemtraip.com/raw.php"
ip = get_ip_from_url(url_check)
data_machine = []

den = "\033[1;90m"
luc = "\033[1;32m"
trang = "\033[1;37m"
red = "\033[1;31m"
vang = "\033[1;33m"
tim = "\033[1;35m"
lamd = "\033[1;34m"
lam = "\033[1;36m"
hong = "\033[1;95m"
reset = "\033[0m"

XNHAC = "\033[38;5;117m"
XANH_DUONG = XNHAC
TRANG_SANG = "\033[97m"
LUC = "\033[92m"
VANG = "\033[93m"
VANG_NHAT = "\033[33m"
DO_NHAT = "\033[91m"
XANH_LA = "\033[96m"
MAGENTA = "\033[95m"
RESET = "\033[0m"

ENC_COLORS = {
    "ASCII/UTF-8": "\033[96m",
    "UTF-16LE": "\033[93m",
    "GAPPED": "\033[95m",
}

kt_code = "</>"
edit = vang + "]" + trang + "[" + red + "[⟨⟩]" + trang + "]" + vang + "[" + trang + " ➩ " + luc
edit1 = trang + "[" + red + "[⟨⟩]" + trang + "]" + trang + " ➩ " + luc

os.system("cls" if os.name == "nt" else "clear")
sleep(1)

banner = f"""
\033[1;34m╔═════════════════════════════════════════════════════════════════╗
\033[1;32m║  █████╗ ██████╗ ██╗██████╗ ███████╗██╗   ██╗                   ║
\033[1;35m║ ██╔══██╗██╔══██╗██║██╔══██╗██╔════╝╚██╗ ██╔╝                   ║
\033[1;31m║ ███████║██████╔╝██║██║  ██║█████╗   ╚████╔╝                    ║
\033[1;33m║ ██╔══██║██╔═══╝ ██║██║  ██║██╔══╝    ╚██╔╝                     ║
\033[1;34m║ ██║  ██║██║     ██║██████╔╝███████╗   ██║                      ║
\033[1;37m║ ╚═╝  ╚═╝╚═╝     ╚═╝╚═════╝ ╚══════╝   ╚═╝                      ║
\033[1;34m╠═════════════════════════════════════════════════════════════════╣
\033[1;32m║➢ Author   : APIDev Tool                                          ║
\033[1;36m║➢ Youtube  : https://youtube.com/@APIDev-ThienNhan               ║
\033[1;31m║➣ Nhóm Zalo: https://zalo.me/g/pxwhiq299                         ║
\033[1;33m║➣ Website  : https://devthiennhan.bio.link                       ║
\033[1;35m║➣ IP Hiện Tại: {vang}{ip:<43}{trang}║
\033[1;36m║➣ Ngày: {red}{ngay_hom_nay}{vang} | {luc}Tháng: {red}{thang_nay}{vang} | {luc}Năm: {red}{nam_}{vang}{" " * 17}║
\033[1;34m╚═════════════════════════════════════════════════════════════════╝
"""

print(banner)

class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
try:
    ssl._create_default_https_context = ssl._create_unverified_context
except Exception:
    pass

r = requests.Session()
r.cookies.set_policy(BlockCookies())

__domains = [
    "api22-core-c-useast1a.tiktokv.com",
    "api19-core-c-useast1a.tiktokv.com",
    "api16-core-c-useast1a.tiktokv.com",
    "api21-core-c-useast1a.tiktokv.com"
]
__devices = [
    "SM-G9900", "SM-A136U1", "SM-M225FV", "SM-E426B", "SM-M526BR",
    "SM-M326B", "SM-A528B", "SM-F711B", "SM-F926B", "SM-A037G",
    "SM-A225F", "SM-M325FV", "SM-A226B", "SM-M426B", "SM-A525F", "SM-N976N"
]
__versions = ["190303", "190205", "190204", "190103", "180904", "180804", "180803", "180802", "270204"]

class Gorgon:
    def __init__(self, params: str, data: str, cookies: str, unix: int) -> None:
        self.unix = unix
        self.params = params
        self.data = data
        self.cookies = cookies
    def hash(self, data: str) -> str:
        try:
            _hash = str(hashlib.md5(data.encode()).hexdigest())
        except Exception:
            _hash = str(hashlib.md5(data).hexdigest())
        return _hash
    def get_base_string(self) -> str:
        base_str = self.hash(self.params)
        base_str = base_str + self.hash(self.data) if self.data else base_str + str('0'*32)
        base_str = base_str + self.hash(self.cookies) if self.cookies else base_str + str('0'*32)
        return base_str
    def get_value(self) -> json:
        base_str = self.get_base_string()
        return self.encrypt(base_str)
    def encrypt(self, data: str) -> json:
        unix = self.unix
        length = 20
        key = [223,119,185,64,185,155,132,131,209,185,203,209,247,194,185,133,195,208,251,195]
        param_list = []
        for i in range(0, 12, 4):
            temp = data[8*i:8*(i+1)]
            for j in range(4):
                H = int(temp[j*2:(j+1)*2], 16)
                param_list.append(H)
        param_list.extend([0,6,11,28])
        H = int(hex(unix), 16)
        param_list.append((H & 4278190080) >> 24)
        param_list.append((H & 16711680) >> 16)
        param_list.append((H & 65280) >> 8)
        param_list.append((H & 255) >> 0)
        eor_result_list = []
        for (A, B) in zip(param_list, key):
            eor_result_list.append(A ^ B)
        for i in range(length):
            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i+1) % length]
            E = C ^ D
            F = self.rbit_algorithm(E)
            H = (F ^ 4294967295 ^ length) & 255
            eor_result_list[i] = H
        result = ''
        for param in eor_result_list:
            result += self.hex_string(param)
        return {'X-Gorgon': '0404b0d30000' + result, 'X-Khronos': str(unix)}
    def rbit_algorithm(self, num):
        result = ''
        tmp_string = bin(num)[2:]
        while len(tmp_string) < 8:
            tmp_string = '0' + tmp_string
        for i in range(0, 8):
            result = result + tmp_string[7 - i]
        return int(result, 2)
    def hex_string(self, num):
        tmp_string = hex(num)[2:]
        if len(tmp_string) < 2:
            tmp_string = '0' + tmp_string
        return tmp_string
    def reverse(self, num):
        tmp_string = self.hex_string(num)
        return int(tmp_string[1:] + tmp_string[:1], 16)

def send(__device_id, __install_id, cdid, openudid):
    global reqs, _lock, success, fails, rps, rpm
    for x in range(10):
        try:
            version = random.choice(__versions)
            params = urlencode({
                "os_api": "25", "device_type": random.choice(__devices), "ssmix": "a",
                "manifest_version_code": version, "dpi": "240", "region": "VN", "carrier_region": "VN",
                "app_name": "musically_go", "version_name": "27.2.4", "timezone_offset": "-28800",
                "ab_version": "27.2.4", "ac2": "wifi", "ac": "wifi", "app_type": "normal", "channel": "googleplay",
                "update_version_code": version, "device_platform": "android", "iid": __install_id,
                "build_number": "27.2.4", "locale": "vi", "op_region": "VN", "version_code": version,
                "timezone_name": "Asia/Ho_Chi_Minh", "device_id": __device_id, "sys_region": "VN",
                "app_language": "vi", "resolution": "720*1280", "device_brand": "samsung", "language": "vi",
                "os_version": "7.1.2", "aid": "1340"
            })
            payload = f"item_id={__aweme_id}&play_delta=1"
            sig = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()
            proxy = random.choice(proxies) if config['proxy']['use-proxy'] else ""
            response = r.post(
                url="https://" + random.choice(__domains) + "/aweme/v1/aweme/stats/?" + params,
                data=payload,
                headers={'cookie': 'sessionid=90c38a59d8076ea0fbc01c8643efbe47',
                         'x-gorgon': sig['X-Gorgon'], 'x-khronos': sig['X-Khronos'], 'user-agent': 'okhttp/3.10.0.1'},
                verify=False,
                proxies={"http": proxy_format + proxy, "https": proxy_format + proxy} if config['proxy']['use-proxy'] else {}
            )
            reqs += 1
            try:
                if response.json()['status_code'] == 0:
                    _lock.acquire()
                    print(f'{red}[{vang}APIDev - ThienNhan{red}] {red}[{luc}BUFF VIEW SUCCESS{red}] {red}{lam}+: {trang}{success}{red} View')
                    success += 1
                    _lock.release()
            except:
                if _lock.locked():
                    _lock.release()
                fails += 1
                continue
        except Exception:
            pass

def rpsm_loop():
    global rps, rpm
    while True:
        initial = reqs
        time.sleep(1.5)
        rps = round((reqs - initial) / 1.5, 1)
        rpm = round(rps * 60, 1)

def fetch_proxies():
    url_list = [
        "https://raw.githubusercontent.com/yemixzy/proxy-list/main/proxy-list/data.txt",
        "https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/http.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks4.txt",
        "https://raw.githubusercontent.com/rdavydov/proxy-list/main/proxies/socks5.txt"
    ]
    for url in url_list:
        try:
            response = requests.get(url, timeout=5)
            if response.ok:
                with open("proxies.txt", "a+", encoding="utf-8") as f:
                    f.write(response.text)
        except:
            pass

if __name__ == "__main__":
    with open('devices.txt', 'r') as f:
        devices = f.read().splitlines()
    with open('config.json', 'r') as f:
        config = json.load(f)
    if config["proxy"]['proxyscrape']:
        fetch_proxies()
    proxy_format = f'{config["proxy"]["proxy-type"].lower()}://{config["proxy"]["credential"]+"@" if config["proxy"]["auth"] else ""}' if config['proxy']['use-proxy'] else ''
    if config['proxy']['use-proxy']:
        with open('proxies.txt', 'r') as f:
            proxies = f.read().splitlines()
    os.system("cls" if os.name == "nt" else "clear")
    print(banner)
    try:
        link = input(f'{red}[{trang}{kt_code}{red}] {luc}INPUT LINK VIDEO: {trang}')
        print(f'{trang}- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
        __aweme_id = str(
            re.findall(r"(\d{18,19})", link)[0]
            if len(re.findall(r"(\d{18,19})", link)) == 1
            else re.findall(r"(\d{18,19})", requests.head(link, allow_redirects=True, timeout=5).url)[0]
        )
    except:
        exit(f"{red}[{trang}{kt_code}{red}] {red}INVALID LINK")
    _lock = threading.Lock()
    reqs = 0
    success = 0
    fails = 0
    rpm = 0
    rps = 0
    threading.Thread(target=rpsm_loop).start()
    while True:
        device = random.choice(devices)
        if eval(base64.b64decode("dGhyZWFkaW5nLmFjdGl2ZV9jb3VudCgpIDwgMTAwICMgZG9uJ3QgY2hhbmdlIGNvdW50IG9yIHUgd2lsbCBraWxsIGRldmljZXMgYW5kIHJ1aW4gZnVuIGZvciBvdGhlcnM=")):
            did, iid, cdid, openudid = device.split(':')
            eval(base64.b64decode("dGhyZWFkaW5nLlRocmVhZCh0YXJnZXQ9c2VuZCxhcmdzPVtkaWQsaWlkLGNkaWQsb3BlbnVkaWRdKS5zdGFydCgp"))
