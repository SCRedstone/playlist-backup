''' PLAYLIST BACKUP creates backups for YouTube and Soundcloud '''

import json
from datetime import datetime
import PySimpleGUI as sg
from utils.errorPopupUtil import error
from utils.playlistGetUtil import sc_get, yt_get


# MAIN PROGRAM
def backupMaker(playlistID):

    # Get API keys from file
    with open("./config.json") as f:
        keys = json.load(f)
    CLIENT_ID = keys["client_id"]
    DEVELOPER_KEY = keys["YT_devkey"]
    savePath = keys["savePath"]

    extracted, client, title = "", "", "<PLAYLIST NAME>"  # Init
    if playlistID.isdigit():  # If playlistID is an integer
        playlistID = int(playlistID)
        if CLIENT_ID == "":
            error("Soundcloud API key is missing! Please check your settings.")
            return
        extracted, title = sc_get(playlistID, CLIENT_ID)
        client = "SC"
    else:  # Otherwise it's a string
        if DEVELOPER_KEY == "":
            error("YouTube API key is missing! Please check your settings.")
            return
        extracted, title = yt_get(playlistID, DEVELOPER_KEY)
        client = "YT"

    # File saving
    fileName = savePath + client + "-" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".json"
    with open(fileName, 'w', encoding='utf8') as outfile:
        json.dump(extracted, outfile, indent=2, ensure_ascii=False)
    sg.Popup(title + ' has been successfully saved to "' + fileName + '"', title="Result")
