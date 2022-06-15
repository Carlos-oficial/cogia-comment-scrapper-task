import lib.tiktok_client,services.tiktok_mappers,json
import lib.instagram_client,services.instagram_mappers,json


# comments_object = lib.tiktok_client.get_comments("7080122963470601477")
# res = models.tiktok_mapper.map_post(comments_object, "description", lib.tiktok_client.get_replies)
# with open('tiktok.json', "w") as file:
#         file.write(json.dumps(res,indent=2))
with open('output.json',) as file:
	post_object = json.load(file)

res = models.instagram_mappers.map_post(post_object)
print(res)
with open('insta.json', "w") as file:
	file.write(json.dumps(res,indent=2))