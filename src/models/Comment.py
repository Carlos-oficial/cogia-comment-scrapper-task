from lib.client import get_replies

class Comment():
    def __init__(self, text, replies=[]):
        self.text = text  # string that holds the comment
        self.replies = replies  # list of strings that holds the replies


def map_comment(response_obj):
    result_dict = []
    for page in response_obj:
        for item in page["items"]:
            main_comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            comment_id = item["id"]
            result_dict.append({"main_comment": main_comment, "replies": map_replies(comment_id)})
    return result_dict

def map_replies(comment_id):
    result_list = []
    replies_obj = get_replies(comment_id)
    for page in replies_obj:
        for item in page["items"]:
            comment = item["snippet"]["textOriginal"]
            result_list.append(comment)
    return result_list