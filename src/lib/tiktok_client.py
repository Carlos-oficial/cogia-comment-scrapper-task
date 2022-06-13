import requests
import json

referer = "https://www.tiktok.com/"
url = "https://www.tiktok.com/api/comment/list/?aweme_id={video_id}&count={n_comments}"
#aweme_id == item_id


def get_post(post_id, comments=100):
    headersList = {
        "Accept": "*/*",
        "Referer": "https://www.tiktok.com/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0" 
    }

    cursor = 0
    i = 0

    reqUrl = f"https://www.tiktok.com/api/comment/list/?aweme_id={post_id}&count={comments}&cursor={cursor}"
    response = [requests.request("GET", reqUrl, headers=headersList).json()]

    while(cursor<response[i]["total"]):
        comments = min (comments,response[i]["total"]-cursor)
        cursor += comments
        total = response[i]["total"]
        print(f"cursor:{cursor},total:{total}")
        reqUrl = f"https://www.tiktok.com/api/comment/list/?aweme_id={post_id}&count={comments}&cursor={cursor}"
        response.append(requests.request("GET", reqUrl, headers=headersList).json())
    return response

post = get_post("7080122963470601477")

with open('output.json', "w") as file:
    file.write(json.dumps((post), sort_keys=True, indent=2))


