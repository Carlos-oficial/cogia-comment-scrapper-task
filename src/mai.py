import lib.tiktok_client,models.tiktok_mapper,json


comments_object = lib.tiktok_client.get_comments("7080122963470601477")
res = models.tiktok_mapper.map_post(comments_object, "description", lib.tiktok_client.get_replies)
with open('tiktok.json', "w") as file:
        file.write(json.dumps(res,indent=2))