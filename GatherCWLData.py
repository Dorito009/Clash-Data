import json
import os
from datetime import datetime
import requests

api_key = os.getenv("COC_API_KEY")
clan_tag = "#2QGYR0GU2"
headers = {
    "Authorization": f"Bearer {api_key}"
}
clan_tag_enc = clan_tag.replace("#", "%23")
url = f'https://cocproxy.royaleapi.dev/v1/clans/{clan_tag_enc}/currentwar/leaguegroup'
warurl = f'https://cocproxy.royaleapi.dev/v1/clanwarleagues/wars/'

response = requests.get(url, headers=headers)
data = response.json()
data.pop("clans")

rounds = data.get("rounds")
data.pop("rounds")
write_data = data

write_data["Tags"] = []
write_data["rounds"] = []
if rounds:
    for rnd in rounds:
        for tag in rnd.get('warTags'):
            if tag != "#0":
                tag_enc = tag.replace("#", "%23")
                war_data = requests.get(warurl + tag_enc, headers=headers).json()
                if war_data.get("clan").get("tag") == clan_tag or war_data.get("opponent").get("tag") == clan_tag:
                    write_data["Tags"].append(tag)
                    write_data["rounds"].append(war_data)





with open(f"data/cwl/cwl-{data.get("season")}.json", "w") as f:
    json.dump(write_data, f, indent=2)