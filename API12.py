import requests
from bs4 import BeautifulSoup
import time


def get_temp_email():
    url = "https://10minutemail.net/?lang=vi"
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    session = requests.Session()
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        email_input = soup.find("input", {"id": "fe_text"})
        email = email_input["value"] if email_input else "Không lấy được email"

        return email, session.cookies.get_dict()
    else:
        return "Lỗi kết nối", {}


def keep_email_alive(cookies):
    url = "https://10minutemail.net/mailbox.ajax.php?_="
    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    session = requests.Session()
    session.cookies.update(cookies)

    while True:
        response = session.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            mails = soup.find_all("tr",
                                  style="font-weight: bold; cursor: pointer;")
            for mail in mails:
                sender = mail.find("a", class_="row-link").text.strip()
                content = mail.find_all("a", class_="row-link")[1].text.strip()
                print(f"Người gửi: {sender} | Nội dung: {content}")
        else:
            print("Lỗi kết nối tới mailbox")
        time.sleep(10)


if __name__ == "__main__":
    email, cookies = get_temp_email()
    print(f"Email tạm thời: {email}")
    keep_email_alive(cookies)
