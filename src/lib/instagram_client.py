import base64
import binascii
import datetime
import struct

from Cryptodome import Random
from Cryptodome.Cipher import AES
from nacl.public import PublicKey, SealedBox
import requests
import json
import os
from loguru import logger
"https://instagram.com/data/shared_data/"

endpoint = "https://instagram.com/accounts/login/ajax/"


# headers = {
#         "User-Agent": "Instagram 10.3.2 (iPhone7,2; iPhone OS 9_3_3; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+",
#         "Referer": "https://instagram.com/",
#         "Origin" : "https://instagram.com/",
#         "Cookie":f"csrftoken={csrf};",
#         "x-csrftoken": csrf
#     }


def is_file_empty(file_path):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0


def shortcode_to_id(shortcode):
    code = ('A' * (12-len(shortcode)))+shortcode
    return int.from_bytes(base64.b64decode(code.encode(), b'-_'), 'big')


def retrieve_id_form_link(link):
    return shortcode_to_id(link.split("/p/")[1])


def get_shared_data():
    req = requests.get("https://www.instagram.com/data/shared_data/").json()
    encryption = req["encryption"]
    csrf = req["config"]["csrf_token"]
    return encryption, csrf


def encrypt_password(key_id: str | int = None, public_key: str = None, version: int = 10, password: str = None) -> str:
    """Password Encryption function for Instagram Login"""

    key_id = int(key_id)
    key = Random.get_random_bytes(32)
    iv = bytes([0] * 12)

    time = int(datetime.datetime.now().timestamp())

    aes = AES.new(key, AES.MODE_GCM, nonce=iv, mac_len=16)
    aes.update(str(time).encode("utf-8"))
    encrypted_password, cipher_tag = aes.encrypt_and_digest(
        password.encode("utf-8"))

    pub_key_bytes = binascii.unhexlify(public_key)
    seal_box = SealedBox(PublicKey(pub_key_bytes))
    encrypted_key = seal_box.encrypt(key)

    encrypted = bytes(
        [
            1,
            key_id,
            *list(struct.pack("<h", len(encrypted_key))),
            *list(encrypted_key),
            *list(cipher_tag),
            *list(encrypted_password),
        ]
    )

    encrypted = base64.b64encode(encrypted)
    encryptedStr = encrypted.decode("utf-8")

    return f"#PWD_INSTAGRAM_BROWSER:{version}:{time}:{encryptedStr}"


def login(username, password):
    session = get_login_creds(username)
    if session:
        print("Session found")
        return session

    enc, csrf = get_shared_data()
    account = {
        'username': username,
        'enc_password': encrypt_password(**enc, password=password)
    }
    headers = {
        "User-Agent": "Instagram 10.3.2 (iPhone7,2; iPhone OS 9_3_3; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+",
        "Referer": "https://instagram.com/",
        "Origin": "https://instagram.com/",
        "Cookie": f"csrftoken={csrf};",
        "x-csrftoken": csrf
    }

    response = requests.post(endpoint, data=account, headers=headers)
    body = response.json()

    if "authenticated" in body.keys() and body["authenticated"]:
        print("authenticated")

        add_session_to_file(username, response.cookies)

    return response.cookies


def add_session_to_file(username, cookies, path='./accounts.json'):

    accounts = {}
    with open(path, "w") as accounts_file:
        if not is_file_empty(path):
            try:
                accounts = json.load(accounts_file)
            except json.JSONDecodeError:
                pass

        accounts[username] = {
            "sessionid": cookies["sessionid"],
            "csrftoken": cookies["csrftoken"]
        }

        print("Session Added")
        accounts_file.write(json.dumps(accounts))


def get_login_creds(username, path='./accounts.json'):
    accounts = {}
    with open(path, "w") as accounts_file:
        if not is_file_empty(path):
            try:
                accounts = json.load(accounts_file)
                accounts_file.write(json.dumps(accounts))
            except json.JSONDecodeError:
                pass
            if username in accounts.keys():
                return accounts[username]
            else:
                return None


def get_comments(session_id, csrf, slug):
    headers = {
        "User-Agent": "Instagram 10.3.2 (iPhone7,2; iPhone OS 9_3_3; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+",
        "Referer": "https://instagram.com/",
        "Origin": "https://instagram.com/",
        "Cookie": f"csrftoken={csrf};sessionid={session_id}",
        "x-csrftoken": csrf
    }
    media_id = shortcode_to_id(slug)
    url = f"https://i.instagram.com/api/v1/media/{media_id}/comments/?can_support_threading=true&permalink_enabled=false"
    result = [requests.get(url, headers=headers).json()]
    i = 0
    # while "next_min_id" in result[i].keys():
    #     next_min_id = result[i]["next_min_id"]
    #     result.append(requests.get(url+f"&min_id={next_min_id}", headers=headers).json())
    #     i += 1
    return result


def main():
    resp_cookies = login("streammanager96", "Portos06241!")
    logger.error("session cookies: {}", resp_cookies)
#     res = get_comments(resp_cookies["sessionid"],
#           resp_cookies["csrftoken"], "CHFjuOdjVIF")
#     print(res)
#     with open('output.json', "w") as file:
#         file.write(json.dumps(res,indent=2))
# #


if __name__ == "__main__":
    main()

# <RequestsCookieJar[<Cookie csrftoken=98ATflSRmIDnOjW2uFVTeUtejmmvfEiD for instagram.com/>, <Cookie ds_user_id=8572570818 for instagram.com/>, <Cookie mid=YqjxYQAAAAFqJFHxJcdt9wv9ynKS for instagram.com/>, <Cookie rur=ASH for instagram.com/>, <Cookie sessionid=8572570818%3A57B6JYaLGT9lVv%3A25 for instagram.com/>]>
