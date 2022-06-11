# modulo com a comunicação com os websites

from googleapiclient.discovery import build
import googleapiclient.discovery
import os

google_API_key = "AIzaSyBkdWcnpyh2NhozpGVYn1xbpk6XCRYmyC4"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def get_comments(vid_id):
    result = []
    with build("youtube", "v3", developerKey=google_API_key) as service:
        request = service.commentThreads().list(
            part="snippet,replies",
            videoId=vid_id,
            maxResults=100)

        req = request.execute()
        result.append(req)
        while "nextPageToken" in req.keys():
            request = service.commentThreads().list(
                part="snippet,replies",
                videoId=vid_id,
                pageToken=req["nextPageToken"],
                maxResults=100)
            req = request.execute()
            result.append(req)

    return result


def get_replies(comment_id):
    result = []
    with build("youtube", "v3", developerKey=google_API_key) as service:
        request = service.comments().list(
            part="snippet",
            parentId=comment_id,
            maxResults=10)
        req = request.execute()
        result.append(req)
        while "nextPageToken" in req.keys():
            request = service.comments().list(
                part="snippet",
                parentId=comment_id,
                pageToken=req["nextPageToken"],
                maxResults=10)
            req = request.execute()
            result.append(req)
    return result
