import requests,json
from bs4 import BeautifulSoup

referer = "https://www.tiktok.com/"
url = "https://www.tiktok.com/api/comment/list/?aweme_id={video_id}&count={n_comments}"
#aweme_id == item_id

def extract_desc(link):

    headersList = {
        "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }

    rep = requests.request("GET", link, headers=headersList).content
    soup =  BeautifulSoup(rep,features="html5lib")
    title = soup.find('title')
    return title.contents[0]

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

def get_replies(comment_id,replies = 100):
    headersList = {
        "Accept": "*/*",
        "Referer": "https://www.tiktok.com/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0" 
    }

    cursor = 0
    i = 0

    reqUrl = f"https://www.tiktok.com/api/comment/list/?aweme_id={comment_id}&count={replies}&cursor={cursor}"
    response = [requests.request("GET", reqUrl, headers=headersList).json()]

    while(cursor<response[i]["total"]):
        replies = min (replies,response[i]["total"]-cursor)
        cursor += replies
        total = response[i]["total"]
        print(f"cursor:{cursor},total:{total}")
        reqUrl = f"https://www.tiktok.com/api/comment/list/?comment_id={comment_id}&count={replies}&cursor={cursor}"
        response.append(requests.request("GET", reqUrl, headers=headersList).json())
    return response

def main():
    extract_desc("https://www.tiktok.com/@jacobfeldmanshow/video/7106632954981403947")


if __name__ == "__main__":
    main()
