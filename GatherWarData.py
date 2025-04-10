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
url = f'https://cocproxy.royaleapi.dev/v1/clans/{clan_tag_enc}/currentwar'

response = requests.get(url, headers=headers)
data = response.json()

if data:
    time_stamp = data.get("startTime")
    if time_stamp:
        dt = datetime.strptime(time_stamp, "%Y%m%dT%H%M%S.%fZ")
        date_str = dt.strftime("%Y-%m-%d")
        with open(f"data/wars/War-{date_str}.json", "w") as f:
            json.dump(data, f, indent=2)
