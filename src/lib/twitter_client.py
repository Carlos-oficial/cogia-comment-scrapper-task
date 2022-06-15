import tweepy
import json
import requests
import os

twitter_API_key = "BRCp0BiQf4StVl3GJhA6tsjjs"
twitter_API_key_secret = "5rnQptxaYqmrEQ8aIQeUeKVxxUvlqi4z4pn5IAbp3e4Z6A1GjG"
twitter_bearer_token = "AAAAAAAAAAAAAAAAAAAAAPuvdgEAAAAARQn2v19kE7hieZbz%2BKZl6duyFOU%3Dad6ZxqI6pCxCk7RBAsizlDqqFoOZGEt2SdqHRoFTRhydX79JJv"
twitter_access_token = "1536044715191279619-3Lf1pDVsk9TICnLljkzkE6ouIC4B3H"
twitter_access_token_secret = "ZSsrsW0LH5oVdI3k51N7sguhBmHGKZd4FcwvtXASyrV6M"

auth = tweepy.OAuthHandler(twitter_API_key, twitter_API_key_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)

api = tweepy.API(auth)

def retrieve_id_form_link(link):
    return link.split("status/")[1]

def create_tweet_req_url(post_id):
    tweet_fields = "tweet.fields=created_at,author_id,text,conversation_id"
    ids = "ids="+post_id
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url

def create_username_req_url(user_id):
    tweet_fields = "tweet.fields=created_at,author_id,text"
    ids = "ids="+user_id
    url = "https://api.twitter.com/2/users?{}".format(ids)
    return url


def create_conversation_req_url(converstion_id,page_token = None):
    query = "query=conversation_id%3A"+converstion_id
    if page_token is not None:
        query += "&pagination_token=" + page_token
    url = "https://api.twitter.com/2/tweets/search/recent?{}".format(query)

    return url


def connect_to_endpoint_bearer(url):
    def bearer_oauth(r):
        r.headers["Authorization"] = f"Bearer {twitter_bearer_token}"
        r.headers["User-Agent"] = "v2TweetLookupPython"
        return r
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_tweet(post_id):
    url = create_tweet_req_url(post_id)
    return connect_to_endpoint_bearer(url)["data"][0]


def get_username(user_id):
    url = create_username_req_url(user_id)
    return connect_to_endpoint_bearer(url)["data"][0]["name"]


def get_conversation(converstion_id,):
    url = create_conversation_req_url(converstion_id)
    result = [connect_to_endpoint_bearer(url)]
    i = 0
    while "next_token" in result[i]["meta"].keys():
        result.append(connect_to_endpoint_bearer(create_conversation_req_url(converstion_id,result[i]["meta"]["next_token"])))
        i += 1
    return result

# replies = []
# for tweet in tweepy.Cursor(api.search_tweets,q='to:'+"NASAKennedy", result_type='recent', timeout=999999).items(1000):
#     if hasattr(tweet, 'in_reply_to_status_id_str'):
#         if (tweet.in_reply_to_status_id_str==tweet_id):
#             replies.append(tweet)
