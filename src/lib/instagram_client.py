import base64
import binascii
import datetime
import struct

from Cryptodome import Random
from Cryptodome.Cipher import AES
from nacl.public import PublicKey, SealedBox
import requests
import json

"https://instagram.com/data/shared_data/"

endpoint = "https://instagram.com/accounts/login/ajax/"



# headers = {
#         "User-Agent": "Instagram 10.3.2 (iPhone7,2; iPhone OS 9_3_3; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+",
#         "Referer": "https://instagram.com/",
#         "Origin" : "https://instagram.com/",
#         "Cookie":f"csrftoken={csrf};",
#         "x-csrftoken": csrf
#     }


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
    print(headers)

    response = requests.post(endpoint, data=account, headers=headers)
    body = response.json()
    if "authenticated" in body.keys() and body["authenticated"]:
        print("authenticated")
    return response.cookies

# https://i.instagram.com/api/v1/media/{media_id}/comments/?can_support_threading=true&permalink_enabled=false
# ^^ request para os cometarios ^^

# headers = {
#         "User-Agent": "Instagram 10.3.2 (iPhone7,2; iPhone OS 9_3_3; en_US; en-US; scale=2.00; 750x1334) AppleWebKit/420+",
#         "Referer": "https://instagram.com/",
#         "Origin" : "https://instagram.com/",
#         "Cookie":f"csrftoken={csrf};sessionid={sesion_id_token}",
#         "x-csrftoken": csrf
#     }

# id_to_shortcode = lambda instagram_id: base64.b64encode(instagram_id.to_bytes(9, 'big'), b'-_').decode().replace('A', ' ').lstrip().replace(' ', 'A')


def shortcode_to_id(shortcode):
    code = ('A' * (12-len(shortcode)))+shortcode
    return int.from_bytes(base64.b64decode(code.encode(), b'-_'), 'big')


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
    while "next_min_id" in result[i].keys():
        next_min_id = result[i]["next_min_id"]
        result.append(requests.get(url+f"&min_id={next_min_id}", headers=headers).json())
        i += 1
        sleep(5000)
    return result

#paginacao
#https://i.instagram.com/api/v1/media/2433508281915625989/comments/?can_support_threading=true&min_id={next_min_id}

def main():
    resp_cookies = login("streammanager96", "Portos06241!")
    res = get_comments(resp_cookies["sessionid"],
          resp_cookies["csrftoken"], "CHFjuOdjVIF")
    print(res)
    with open('output.json', "w") as file:
        file.write(res)


if __name__ == "__main__":
    main()

