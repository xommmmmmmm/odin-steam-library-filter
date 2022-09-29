# 1. Go to https://steamid.io/ and lookup your steamID64
# 2. Replace <steamID64> with the value from 1. and go to https://steamcommunity.com/profiles/<steamID64>/games?tab=all&xml=1
# 3. Save that as games.xml in the same folder as this script
# 4. Run pip install -r requirements.txt to install the two dependencies
# 5. Run python gamelookup.py to generate your CSV

import time
import json, csv

import requests
import xmltodict

result = []

# Load XML as dictionary
with open("games.xml", "r", encoding="utf-8") as f:
    j = xmltodict.parse(f.read())

# Iterate through games
num_games = len(j["gamesList"]["games"]["game"])
for i, app in enumerate(j["gamesList"]["games"]["game"]):
    appid = app["appID"]

    # Retrieve info from PCGamingWiki
    # https://www.pcgamingwiki.com/wiki/PCGamingWiki:API
    # https://www.pcgamingwiki.com/wiki/Special:CargoTables
    # https://www.mediawiki.org/wiki/Extension:Cargo/Querying_data

    x = requests.get("https://www.pcgamingwiki.com/w/api.php", params={
        "action": "cargoquery",
        "tables": "Infobox_game,API,Input",
        "fields": "Infobox_game._pageName=Page,API.Windows_32bit_executable,API.Windows_64bit_executable,Input.Controller_support,Input.Full_controller_support",
        "join_on": "Infobox_game._pageID=API._pageID,Infobox_game._pageID=Input._pageID",
        "where": f"Infobox_game.Steam_AppID HOLDS '{appid}'",
        "format": "json"
    })

    r = {
        "appid": appid,
        "name": app["name"],
        "hours": app.get("hoursOnRecord", 0),
        "storeLink": app["storeLink"]
    }

    # Some games don't have PCGW pages
    try:
        if x.json()["cargoquery"] != []:
            r["32-bit"] = x.json()["cargoquery"][0]["title"]["Windows 32bit executable"]
            r["64-bit"] = x.json()["cargoquery"][0]["title"]["Windows 64bit executable"]
            r["controller"] = x.json()["cargoquery"][0]["title"]["Controller support"]
            r["full_controller"] = x.json()["cargoquery"][0]["title"]["Full controller support"]
        else:
            r["32-bit"] = "not found"
            r["64-bit"] = "not found"
            r["controller"] = "not found"
            r["full_controller"] = "not found"
    except:
        print(x.text)

    # Only save if has 32-bit and controller support
    if (r["32-bit"] == "true" and r["controller"] == "true" ):
        result += [r]
        match = "Matched!"
    else:
        match = "Skipping..."

    print(f"{i}/{num_games} ({round(i/num_games*100, 1)}%):\t{match}\t{appid}\t{app['name']}\t")

    # If you get rate limited, set a sleep time
    # time.sleep(0.05)

# Save as csv for filtering in Excel
with open("output.csv", "w", newline='', encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(result[0].keys())
    for game in result:
        w.writerow(game.values())
