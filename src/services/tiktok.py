
def map_post(comments_object, description,get_replies):
    result = {"comments": []}
    result["text"] = description
    for page in comments_object:
        if "comments" in page.keys() and page["comments"] is not None:
            for comment in page["comments"]:
                comment_dict={}
                comment_dict["text"] = (comment["text"])
                comment_id = (comment["cid"])
                comment_dict["replies"] = map_replies(get_replies(comment_id))
                result["comments"].append(comment_dict)
    return result


def map_replies(comment_object):
    result = []
    for page in comment_object:
        if "comments" in page.keys() and page["comments"] is not None: 
            for reply in page["comments"]:
                result.append(reply["text"])
                print(reply["text"])
    return result


def main():
    req = get_comments("7080122963470601477")
    print(map_post(req))

if __name__ == "__main__":
    main()
