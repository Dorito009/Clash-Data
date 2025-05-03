import json
import os
from copy import deepcopy
from datetime import datetime
import requests

api_key = os.getenv("COC_API_KEY")

player_prefab = {
    "townHallLevel": 0,
    "townHallWeaponLevel": 0,
    "expLevel": 0,
    "trophies": 0,
    "bestTrophies": 0,
    "warStars": 0,
    "attackWins": 0,
    "defenseWins": 0,
    "builderHallLevel": 0,
    "builderBaseTrophies": 0,
    "bestBuilderBaseTrophies": 0,
    "role": "leader",
    "warPreference": "in",
    "donations": 0,
    "donationsReceived": 0,
    "clanCapitalContributions": 0,
    "league": 0
}

clan_tag = "#2QGYR0GU2"

headers = {
    "Authorization": f"Bearer {api_key}"
}
clan_tag_enc = clan_tag.replace("#", "%23")
clan_url = f'https://cocproxy.royaleapi.dev/v1/clans/{clan_tag_enc}'

response = requests.get(clan_url, headers=headers)
data = response.json()

date = datetime.now().strftime("%Y-%m-%d")

if data:
    member_tags = [member["tag"] for member in data["memberList"]]
    for tag in member_tags:
        player_tag_enc = tag.replace("#", "%23")
        player_url = f'https://cocproxy.royaleapi.dev/v1/players/{player_tag_enc}'
        player_response = requests.get(player_url, headers=headers)
        player_data = player_response.json()
        if not player_data:
            continue

        file_path = f"data/members/{tag.replace("#", "")}.json"
        if os.path.exists(file_path):
            with open(file_path) as f:
                player_file = json.load(f)
                player_file["name"] = player_data["name"]
        else:
            player_file = {
                "tag": player_data["tag"],
                "name": player_data["name"],
                "data": {}
            }
        new_player_data = deepcopy(player_prefab)
        for key in player_prefab:
            if key in player_data:
                new_player_data[key] = player_data[key]
        player_file["data"][date] = new_player_data

        with open(file_path, "w") as f:
            json.dump(player_file, f, indent=2)

    data["labels"].pop()
    data["memberList"].pop()
    data["memberList"] = member_tags

    with open(f"data/clan/Clan-{date}.json", "w") as f:
        json.dump(data, f, indent=2)



