
import json
from lib.yt_client import get_comments,get_details
from models.Comment import *

post1 = Yt_Post("youtube",get_details("7qH8prh4hpE"),get_comments("7qH8prh4hpE"))

with open('output.json', "w") as file:
    file.write(json.dumps((post1.__dict__),
               sort_keys=True, indent=2))

