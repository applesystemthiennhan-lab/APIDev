import hashlib
import random
import requests
import time
from datetime import datetime
import json
import sys
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = {
    'api_key': '882a8490361da98702bf97a021ddc14d',
    'secret': '62f8ce9f74b12f84c123cc23437a4a32',
    'key': ['ChanHungCoder_KeyRegFBVIP_9999', 'DCHVIPKEYREG']
}

email_prefix = ['gmail.com', 'hotmail.com', 'yahoo.com', 'outlook.com']


def create_account():
    random_birth_day = datetime.strftime(
        datetime.fromtimestamp(
            random.randint(
                int(
                    time.mktime(
                        datetime.strptime('1980-01-01',
                                          '%Y-%m-%d').timetuple())),
                int(
                    time.mktime(
                        datetime.strptime('1995-12-30',
                                          '%Y-%m-%d').timetuple())))),
        '%Y-%m-%d')

    names = {
        'first': ['JAMES', 'JOHN', 'ROBERT', 'MICHAEL', 'WILLIAM', 'DAVID'],
        'last': ['SMITH', 'JOHNSON', 'WILLIAMS', 'BROWN', 'JONES', 'MILLER'],
        'mid': ['Alexander', 'Anthony', 'Charles', 'Dash', 'David', 'Edward']
    }

    random_first_name = random.choice(names['first'])
    random_name = f"{random.choice(names['mid'])} {random.choice(names['last'])}"
    password = f'HelloReg{random.randint(0, 9999999)}?#@'
    full_name = f"{random_first_name} {random_name}"
    md5_time = hashlib.md5(str(time.time()).encode()).hexdigest()
    hash_ = f"{md5_time[0:8]}-{md5_time[8:12]}-{md5_time[12:16]}-{md5_time[16:20]}-{md5_time[20:32]}"
    email_rand = f"{full_name.replace(' ', '').lower()}{hashlib.md5((str(time.time()) + datetime.strftime(datetime.now(), '%Y%m%d')).encode()).hexdigest()[0:6]}@{random.choice(email_prefix)}"
    gender = 'M' if random.randint(0, 10) > 5 else 'F'

    req = {
        'api_key': app['api_key'],
        'attempt_login': True,
        'birthday': random_birth_day,
        'client_country_code': 'EN',
        'fb_api_caller_class':
        'com.facebook.registration.protocol.RegisterAccountMethod',
        'fb_api_req_friendly_name': 'registerAccount',
        'firstname': random_first_name,
        'format': 'json',
        'gender': gender,
        'lastname': random_name,
        'email': email_rand,
        'locale': 'en_US',
        'method': 'user.register',
        'password': password,
        'reg_instance': hash_,
        'return_multiple_errors': True
    }

    sig = ''.join([f'{k}={v}' for k, v in sorted(req.items())])
    ensig = hashlib.md5((sig + app['secret']).encode()).hexdigest()
    req['sig'] = ensig

    api = 'https://b-api.facebook.com/method/user.register'

    def _call(url='', params=None, post=True):
        headers = {
            'User-Agent':
            '[FBAN/FB4A;FBAV/35.0.0.48.273;FBDM/{density=1.33125,width=800,height=1205};FBLC/en_US;FBCR/;FBPN/com.facebook.katana;FBDV/Nexus 7;FBSV/4.1.1;FBBK/0;]'
        }
        if post:
            response = requests.post(url,
                                     data=params,
                                     headers=headers,
                                     verify=False)
        else:
            response = requests.get(url,
                                    params=params,
                                    headers=headers,
                                    verify=False)
        return response.text

    reg = _call(api, req)
    reg_json = json.loads(reg)
    uid = reg_json.get('session_info', {}).get('uid')
    access_token = reg_json.get('session_info', {}).get('access_token')
    error_code = reg_json.get('error_code')
    error_msg = reg_json.get('error_msg')

    if uid is not None and access_token is not None:
        data_to_save = f"{random_birth_day}:{full_name}:{email_rand}:{password}:{uid}:{access_token}"
        with open("facebook.txt", "a") as file:
            file.write(data_to_save + "\n")

        print("Tạo thành công:")
        print(f"  Date of Birth: {random_birth_day}")
        print(f"  Name         : {full_name}")
        print(f"  Mail         : {email_rand}")
        print(f"  Password     : {password}")
        print(f"  Id           : {uid}")
        print(f"  Token        : {access_token}")
        print()
    else:
        if error_code and error_msg:
            print(f"error: {error_code} - {error_msg}")
        else:
            print("Unknown error")


if __name__ == "__main__":
    try:
        account_count = int(input("Nhập số lượng acc muốn reg: "))
        if account_count <= 0:
            print("Số lượng không được thấp hơn 0.")
            sys.exit(1)
    except ValueError:
        print("Tham số không hợp lệ.")
        sys.exit(1)

    for _ in range(account_count):
        create_account()
        time.sleep(5)

    print(
        "Tất cả tài khoản đã được tạo. Kết quả được lưu trong tệp: facebook.txt"
    )
