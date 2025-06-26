''' PLAYLIST BACKUP creates backups for YouTube and Soundcloud '''

import json
from datetime import datetime
import FreeSimpleGUI as sg
from utils.errorPopupUtil import error
from utils.playlistGetUtil import sc_get, yt_get
from os import makedirs


# MAIN PROGRAM
def backupMaker(playlistID):

    # Get API keys from file
    with open("./config.json") as f:
        keys = json.load(f)
    CLIENT_ID = keys["client_id"]
    CLIENT_SECRET = keys["client_secret"]
    DEVELOPER_KEY = keys["YT_devkey"]
    savePath = keys["savePath"]

    extracted, client, title = "", "", "<PLAYLIST NAME>"  # Init
    if "soundcloud:playlists:" in playlistID:  # If playlistID is Soundcloud
        if CLIENT_ID == "" or CLIENT_SECRET == "":
            error("Soundcloud API key is missing! Please check your settings.")
            return
        extracted, title = sc_get(playlistID, CLIENT_ID, CLIENT_SECRET)
        client = "SC"
        extracted = [extracted, {"playlist-type": "Soundcloud"}]
    else:  # Otherwise it's YouTube ID string
        if DEVELOPER_KEY == "":
            error("YouTube API key is missing! Please check your settings.")
            return
        extracted, title = yt_get(playlistID, DEVELOPER_KEY)
        client = "YT"
        extracted.append({"playlist-type": "YouTube"})

    # File saving
    makedirs(savePath, exist_ok=True)  # Make folder if folder doesn't exist
    savePath = savePath + client + "-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".json"
    with open(savePath, 'w', encoding='utf8') as outfile:
        json.dump(extracted, outfile, indent=2, ensure_ascii=False)
    sg.Popup(title + ' has been successfully saved to "' + savePath + '"', title="Result")
