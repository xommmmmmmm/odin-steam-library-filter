# odin-steam-library-filter

A simple script to filter games with 32-bit versions and controller support for usage on Windows on ARM devices e.g. Ayn Odin.

1. Go to https://steamid.io/ and lookup your steamID64
2. Replace <steamID64> with the value from 1. and go to https://steamcommunity.com/profiles/<steamID64>/games?tab=all&xml=1
3. Save that as games.xml in the same folder as this script
4. Run pip install -r requirements.txt to install the two dependencies
5. Run python gamelookup.py to generate your CSV 
