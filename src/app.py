import json
from lib.parser import parse
import lib.yt_client as yt_client ,services.youtube as yt_services
import lib.twitter_client as twitter_client ,services.twitter as twitter_services

def init_json():
    parse("../task/link_list.xlsx")
    with open('./links.json', "r") as file:
        obj = json.load(file)
    
    new_obj = {}
    for social,cont in obj.items():
        new_obj[social] = {}
        for link in cont:
            new_obj[social][link] = {}

    with open('./reponse.json',"w") as file:
        file.write(json.dumps(new_obj,indent=2))

def get_yt_videos(path = './reponse.json'):
    with open(path, "r") as file:
        obj = json.load(file)
    for key,value in obj['Youtube'].items():
        with open(path, "r") as file:
            obj = json.load(file)
        if not value and "shorts" not in key:
            details_obj = yt_client.get_details(yt_client.retrieve_id_form_link(key))
            obj['Youtube'][key] = yt_services.map_yt_video_details(details_obj)
            obj['Youtube'][key]['comments'] = yt_services.map_comment(yt_client.get_comments(yt_client.retrieve_id_form_link(key)),yt_client.get_replies)
        with open(path, "w") as file:
            file.write(json.dumps(obj,indent=2))

def get_tweets(path = './reponse.json'):
    with open(path, "r") as file:
        obj = json.load(file)
    for (key,value)in obj['Twitter'].items():
        print (key)
        if len(obj['Twitter'][key])==0:
            details_obj = twitter_client.get_tweet(twitter_client.retrieve_id_form_link(key))
            print (json.dumps(details_obj,sort_keys=True,indent=2))
            obj['Twitter'][key] = twitter_services.map_tweet(details_obj,twitter_client.get_conversation)
            print(obj)
        with open(path, "w") as file:
            file.write(json.dumps(obj,indent=2))


# get_yt_videos(path = './reponse.json')      
get_tweets()