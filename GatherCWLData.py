import json
import os
import sys
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

if data.get("state") and data.get("state") != "ended":
    data.pop("clans")
    
    rounds = data.get("rounds")
    data.pop("rounds")
    write_data = data
    
    write_data["tags"] = []
    write_data["clanWars"] = []
    
    write_data["rounds"] = []
    
    if data.get("state") in (["inWar", "preparation", "warEnded"]):
        for rnd in rounds:
            round_array = []
            for tag in rnd.get('warTags'):
                if tag != "#0":
                    tag_enc = tag.replace("#", "%23")
                    war_data = requests.get(warurl + tag_enc, headers=headers).json()
                    if war_data.get("clan").get("tag") == clan_tag or war_data.get("opponent").get("tag") == clan_tag:
                        write_data["tags"].append(tag)
                        write_data["clanWars"].append(war_data)
                    if war_data.get("state") in (["inWar", "preparation", "warEnded"]):
                        round_data = {
                            "warTag": tag,
                            "clan1": {
                                "tag": war_data.get("clan").get("tag"),
                                "name": war_data.get("clan").get("name"),
                                "badgeUrls": war_data.get("clan").get("badgeUrls"),
                                "stars": war_data.get("clan").get("stars"),
                                "attacks": war_data.get("clan").get("attacks"),
                                "destructionPercentage": war_data.get("clan").get("destructionPercentage"),
                            },
                            "clan2": {
                                "tag": war_data.get("opponent").get("tag"),
                                "name": war_data.get("opponent").get("name"),
                                "badgeUrls": war_data.get("opponent").get("badgeUrls"),
                                "stars": war_data.get("opponent").get("stars"),
                                "attacks": war_data.get("opponent").get("attacks"),
                                "destructionPercentage": war_data.get("opponent").get("destructionPercentage"),
                            }
                        }
                        round_array.append(round_data)
            write_data["rounds"].append(round_array)
    
    
    with open(f"data/cwl/cwl-{data.get("season")}.json", "w") as f:
        json.dump(write_data, f, indent=2)
