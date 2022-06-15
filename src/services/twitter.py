def map_tweet(tweet_object,get_conversation):
    result = {}
    result["text"] = tweet_object["text"]
    result["replies"] = map_conversation(get_conversation(tweet_object["conversation_id"]))
    return result

def map_conversation(conversation_object):
    result = []
    for item in conversation_object:
        if "data" in item.keys():
            for tweet in item["data"]:
                result.append(tweet["text"])
    return result