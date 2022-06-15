import requests
import json

def retrieve_id_form_link(link):
    return link.split("video/")[1]


def extract_desc(link):

    headersList = {
        "User-Agent": "Thunder Client (https://www.thunderclient.com)"
    }

    rep = requests.request("GET", link, headers=headersList).content
    soup = BeautifulSoup(rep, features="html5lib")
    title = soup.find('title')
    return title.contents[0]


def get_comments(post_id, comments=100):
    headersList = {
        "Accept": "*/*",
        "Referer": "https://www.tiktok.com/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"
    }
    cursor = 0
    i = 0
    reqUrl = f"https://www.tiktok.com/api/comment/list/?aweme_id={post_id}&count={comments}&cursor={cursor}"
    response = [requests.request("GET", reqUrl, headers=headersList).json()]

    while(cursor < response[i]["total"]):
        comments = min(comments, response[i]["total"]-cursor)
        cursor += comments
        total = response[i]["total"]
        reqUrl = f"https://www.tiktok.com/api/comment/list/?aweme_id={post_id}&count={comments}&cursor={cursor}"
        response.append(requests.request(
            "GET", reqUrl, headers=headersList).json())
    return response


def get_replies(comment_id, replies=100):
    headersList = {
        "Accept": "*/*",
        "Referer": "https://www.tiktok.com/",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0"
    }
    cursor = 0
    i = 0
    reqUrl = f"https://www.tiktok.com/api/comment/list/reply/?comment_id={comment_id}&count={replies}&cursor={cursor}"
    resp = requests.request("GET", reqUrl, headers=headersList)
    try:
        resp = resp.json()
    except requests.exceptions.JSONDecodeError:
        return []

    response = [resp]

    while(response[i]["has_more"]):
        replies = min(replies, response[i]["total"]-cursor)
        cursor += replies
        total = response[i]["total"]

        reqUrl = f"https://www.tiktok.com/api/comment/list/reply/?comment_id={comment_id}&count={replies}&cursor={cursor}"

        resp = requests.request("GET", reqUrl, headers=headersList).json()

        response.append(resp)
        i += 1
    return response


def main():
    pass


if __name__ == "__main__":
    main()
