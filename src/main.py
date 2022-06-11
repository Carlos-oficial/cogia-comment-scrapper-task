
import json
from lib.client import get_comments,get_replies
from models.Comment import *

resp = get_comments("7qH8prh4hpE")
# resp = get_replies("UgxKK_9nII_Pd4dl5094AaABAg")
# print(resp)
reps = (map_comment(resp))
with open('output.json', "w") as file:
    file.write(json.dumps((reps),
               sort_keys=True, indent=2))

