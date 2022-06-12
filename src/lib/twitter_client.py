import tweepy,json,requests,os

twitter_API_key = "BRCp0BiQf4StVl3GJhA6tsjjs"
twitter_API_key_secret = "5rnQptxaYqmrEQ8aIQeUeKVxxUvlqi4z4pn5IAbp3e4Z6A1GjG"
twitter_bearer_token = "AAAAAAAAAAAAAAAAAAAAAPuvdgEAAAAARQn2v19kE7hieZbz%2BKZl6duyFOU%3Dad6ZxqI6pCxCk7RBAsizlDqqFoOZGEt2SdqHRoFTRhydX79JJv"
twitter_access_token = "1536044715191279619-3Lf1pDVsk9TICnLljkzkE6ouIC4B3H"
twitter_access_token_secret = "ZSsrsW0LH5oVdI3k51N7sguhBmHGKZd4FcwvtXASyrV6M"

auth = tweepy.OAuthHandler(twitter_API_key, twitter_API_key_secret)
auth.set_access_token(twitter_access_token, twitter_access_token_secret)

api = tweepy.API(auth)


def create_url(post_id):
    tweet_fields = "tweet.fields=created_at"
    ids = "ids="+post_id
    url = "https://api.twitter.com/2/tweets?{}&{}".format(ids, tweet_fields)
    return url


def bearer_oauth(r):
    r.headers["Authorization"] = f"Bearer {twitter_bearer_token}"
    r.headers["User-Agent"] = "v2TweetLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_tweet(post_id):
    post = {}
    url = create_url(post_id)
    json_response = connect_to_endpoint(url)
    post["tweet"] = json_response["data"][0]["text"]
    post["date"] = json_response["data"][0]["created_at"]
    return (json.dumps(post, indent=4, sort_keys=True))


if __name__ == "__main__":
    print(get_tweet("1486641394735271939"))