from lib.client import get_comments

class Comment():
    def __init__(self, text, replies=[]):
        self.text = text  # string that holds the comment
        self.replies = replies  # list of strings that holds the replies


def map_comment(response_obj):
    result_dict = []
    for item in response_obj["items"]:
        main_comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        result_dict.append({"main_comment": main_comment, "replies": get_replies(item[""])})
    return result_dict

def map_replies(comment_id):
    pass