

def map_post(post_object):
    result = {"comments":[]}
    for page in post_object:
        if "caption" not in result.keys():
            result["caption"]=page["caption"]["text"]
        for comment in page["comments"]:
            result["comments"].append(comment["text"])
    return result