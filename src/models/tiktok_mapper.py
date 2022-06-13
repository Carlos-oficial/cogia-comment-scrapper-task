from lib.tiktok_client import get_replies

def map_post(post_object):
    result = {}
    result["text"] = post_object[0]["comments"]