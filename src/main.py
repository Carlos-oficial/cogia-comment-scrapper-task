
import json
from lib.yt_client import get_comments,get_details

from models.yt_mappers import *
from models.twitter_mappers import map_tweet

# post1 = Yt_Post("youtube",get_details("7qH8prh4hpE"),get_comments("7qH8prh4hpE"))
post2 = map_tweet("1535970795448586242")
with open('output.json', "w") as file:
    file.write(json.dumps((post2),
               sort_keys=True, indent=2))

