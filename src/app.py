import json
from lib.parser import parse
import lib.yt_client as yt_client
import services.youtube as yt_services
import lib.twitter_client as twitter_client
import services.twitter as twitter_services
import lib.tiktok_client as tiktok_client
import services.tiktok as tiktok_services

# file for writing to the result file(s)


def init_json():
    parse("../task/link_list.xlsx")
    with open('./links.json', "r") as file:
        obj = json.load(file)

    new_obj = {}
    for social, cont in obj.items():
        new_obj[social] = {}
        for link in cont:
            new_obj[social][link] = {}

    with open('./reponse.json', "w") as file:
        file.write(json.dumps(new_obj, indent=2))


def get_yt_videos(path='./reponse.json'):
    with open(path, "r") as file:
        obj = json.load(file)
    for key, value in obj['Youtube'].items():
        with open(path, "r") as file:
            obj = json.load(file)
        if not value and "shorts" not in key:
            details_obj = yt_client.get_details(
                yt_client.retrieve_id_form_link(key))
            obj['Youtube'][key] = yt_services.map_yt_video_details(details_obj)
            obj['Youtube'][key]['comments'] = yt_services.map_comment(yt_client.get_comments(
                yt_client.retrieve_id_form_link(key)), yt_client.get_replies)
        with open(path, "w") as file:
            file.write(json.dumps(obj, indent=2))


def get_tweets(path='./reponse.json'):
    with open(path, "r") as file:
        obj = json.load(file)
    for (key, value) in obj['Twitter'].items():
        if len(obj['Twitter'][key]) == 0:
            at = sum(len(item[1]) > 0 for item in obj['Twitter'].items())
            total = len(obj['Twitter'].keys())
            print(f"""
            at:{at}
            total:{total}
            {at/total*100}% done""")
            details_obj = twitter_client.get_tweet(
                twitter_client.retrieve_id_form_link(key))
            obj['Twitter'][key] = twitter_services.map_tweet(
                details_obj, twitter_client.get_conversation)
        with open(path, "w") as file:
            file.write(json.dumps(obj, indent=2))

get_tweets('./Twitter_response.json')

def get_tiktoks(path='./reponse.json'):
    with open(path, "r") as file:
        obj = json.load(file)
    for (key, value) in obj['TikTok'].items():
        if len(obj['TikTok'][key]) == 0:
            at = sum(len(item[1]) > 0 for item in obj['TikTok'].items())
            total = len(obj['TikTok'].keys())
            print(f"""
            at:{at}
            total:{total}
            {at/total*100}% done""")
            description = tiktok_client.extract_desc(key)
            comments = tiktok_client.get_comments(
                tiktok_client.retrieve_id_form_link(key))
            obj['TikTok'][key] = tiktok_services.map_post(
                comments, description, tiktok_client.get_replies)
        with open(path, "w") as file:
            file.write(json.dumps(obj, indent=2))


def split_result(path='./reponse.json'):
    with open(path, "r") as file:
        obj = json.load(file)
    for key, value in obj.items():
        with open(f'./{key}_response.json', "w") as file:
            newobj = {key: value}
            file.write(json.dumps(newobj, indent=2))


def concat_result():
    with open('./TikTok_response.json', "r") as file:
        TikTok_obj = json.load(file)
    with open('./Youtube_response.json', "r") as file:
        Youtube_obj = json.load(file)
    with open('./Instagram_response.json', "r") as file:
        Instagram_obj = json.load(file)
    with open('./Twitter_response.json', "r") as file:
        Twitter_obj = json.load(file)
    with open(f'./response.json', "w") as file:
        newobj = {
            'TikTok': TikTok_obj,
            'Youtube': Youtube_obj,
            'Twitter': Twitter_obj,
            'Instagram': Instagram_obj,
        }
        file.write(json.dumps(newobj, indent=2))


split_result()
