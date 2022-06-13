
import requests
# post1 = Yt_Post("youtube",get_details("7qH8prh4hpE"),get_comments("7qH8prh4hpE"))
# post2 = map_tweet("1535970795448586242")
# with open('output.json', "w") as file:
#     file.write(json.dumps((post2),
#                sort_keys=True, indent=2))

user_agent = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0', 'Referer' : 'https://twitter.com/sw.js' }
url_base = "https://twitter.com/home?precache=1"
r = requests.get(url_base, verify=False, headers=user_agent)
soup = BeautifulSoup(r.text, "html.parser")
js_with_bearer = ""
for i in soup.find_all('link'):
    if i.get("href").find("/main") != -1:
        js_with_bearer = i.get("href")

guest_token = re.findall(r'"gt=\d{19}', str(soup.find_all('script')[-1]), re.IGNORECASE)[0].replace("\"gt=","")
print("[*] Js with Bearer token: %s" % js_with_bearer)
print("[*] Guest token: %s" % guest_token)
# Get Bearer token
user_agent = { 'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0', 'Referer' : 'https://twitter.com/sw.js' }
r = requests.get(js_with_bearer, verify=False, headers=user_agent)
#print(r.text)
bearer = re.findall(r'",[a-z]="(.*)",[a-z]="\d{8}"', r.text, re.IGNORECASE)[0].split("\"")[-1]
print("[*] Bearer: %s" % bearer)

rt_path = re.search(r'queryId:"(.+?)",operationName:"Retweeters"', r.text).group(1).split('"')[-1]
viewer_path = re.search(r'queryId:"(.+?)",operationName:"Viewer"', r.text).group(1).split('"')[-1]
print("[*] rt_url: %s" % rt_path)
authorization_bearer = "Bearer %s" % bearer