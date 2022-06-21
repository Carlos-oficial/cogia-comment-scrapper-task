import json

import lib.yt_client as yt_client
import lib.twitter_client as twitter_client
import lib.tiktok_client as tiktok_client
import lib.instagram_client as instagram_client
import services.youtube as yt_services
import services.twitter as twitter_services
import services.tiktok as tiktok_services
import services.instagram as instagram_services


def get_yt_video(link, save_if_not_found=False):
    obj = {}
    with open('response.json', 'r') as file:
        content = json.load(file)
        if link in content['Youtube'].keys():
            if len(content['Youtube'][link]):
                print("in database")
                with open('response.json', 'w') as file:
                    file.write(json.dumps(content, indent=2))
                return content['Youtube'][link]
        details_obj = yt_client.get_details(
            yt_client.retrieve_id_form_link(link))
        obj = yt_services.map_yt_video_details(details_obj)
        obj['comments'] = yt_services.map_comment(yt_client.get_comments(
            yt_client.retrieve_id_form_link(link)), yt_client.get_replies)
        if save_if_not_found:
            content['Youtube'][link] = obj
        with open('response.json', 'w') as file:
            file.write(json.dumps(content, indent=2))
    return obj


def get_tiktok_video(link, save_if_not_found=False):
    obj = {}
    with open('./response.json', 'r') as file:
        content = json.load(file)
        if link in content['TikTok'].keys():
            if len(content['TikTok'][link]):
                print("in database")
                with open('response.json', 'w') as file:
                    file.write(json.dumps(content, indent=2))
                return content['TikTok'][link]
        description = tiktok_client.extract_desc(link)
        comments = tiktok_client.get_comments(
            tiktok_client.retrieve_id_form_link(link))
        obj = tiktok_services.map_post(
            comments, description, tiktok_client.get_replies)
        if save_if_not_found:
            content['TikTok'][link] = obj
        with open('response.json', 'w') as file:
            file.write(json.dumps(content, indent=2))

    return obj


def get_tweet(link, save_if_not_found=False):
    obj = {}
    with open('response.json', 'r') as file:
        content = json.load(file)
        if link in content['Twitter'].keys():
            if len(content['Twitter'][link]):               
                print("in database")
                with open('response.json', 'w') as file:
                    file.write(json.dumps(content, indent=2))
                return content['Twitter'][link]
        details_obj = twitter_client.get_tweet(
            twitter_client.retrieve_id_form_link(link))
        obj = twitter_services.map_tweet(
            details_obj, twitter_client.get_conversation)
        if save_if_not_found:
            content['Twitter'][link] = obj
        with open('response.json', 'w') as file:
            file.write(json.dumps(content, indent=2))
    return obj


def crawl_for_post(link, save_if_not_found = False):
    if "youtube" in link:
        return get_yt_video(link, save_if_not_found)
    elif "twitter" in link:
        return get_tweet(link, save_if_not_found)
    elif "tiktok" in link:
        return get_tiktok_video(link, save_if_not_found)
    # elif "instagram" in link: Not implemented due to inability to test
print(json.dumps(crawl_for_post("https://www.youtube.com/watch?v=3uMoAqFzJ3M"), indent=2))
