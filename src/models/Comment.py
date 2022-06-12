from lib.yt_client import get_replies


class Yt_Post():
    def __init__(self, video_object, comment_thread_list):
            self.post_title = map_yt_video_details(video_object)["title"]
            self.post_description = map_yt_video_details(video_object)["description"]
            self.comments = map_comment(comment_thread_list)

class Comment():
    def __init__(self, text, replies=[]):
        self.text = text  # string that holds the comment
        self.replies = replies  # list of strings that holds the replies


def map_yt_video_details(video_object):
    result_dict = {}
    result_dict["title"] = video_object["video"]["items"][0]["snippet"]["title"]
    result_dict["description"] = video_object["video"]["items"][0]["snippet"]["description"]
    return result_dict


def map_comment(response_obj):
    result_list = []
    for page in response_obj:
        for item in page["items"]:
            main_comment = item["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
            comment_id = item["id"]
            result_list.append(
                {"main_comment": main_comment, "replies": map_replies(comment_id)})
    return result_list


def map_replies(comment_id):
    result_list = []
    replies_obj = get_replies(comment_id)
    for page in replies_obj:
        for item in page["items"]:
            comment = item["snippet"]["textOriginal"]
            result_list.append(comment)
    return result_list

