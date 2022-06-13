from lib.twitter_client import get_tweet, get_conversation

def map_tweet(tweet_object):
    result = {}
    result["text"] = tweet_object["text"]
    result["replies"] = map_conversation(get_conversation(tweet_object["conversation_id"]))
    return result

def map_conversation(conversation_object):
    result = []
    for item in conversation_object:
        for tweet in item["data"]:
            result.append(tweet["text"])
    return result