''' PLAYLIST BACKUP creates backups for YouTube and Soundcloud '''

import json
import os
import time
import urllib.request
from datetime import datetime
import PySimpleGUI as sg
import googleapiclient.discovery
import googleapiclient.errors
from utils.extract import json_extract


def sc_get(set_id, CLIENT_ID):
    with urllib.request.urlopen("https://api.soundcloud.com/playlists/" + str(set_id) + "?client_id=" + CLIENT_ID) as url:
        playlist = json.loads(url.read().decode())
    return playlist


def yt_get(set_id, DEVELOPER_KEY):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)
    pageToken = ""  # Stores the next page token
    extractedToken = [""]  # Stores the next page token as a list to test loop condition
    result = []
    counter = 0
    while extractedToken:  # If there is a next page
        time.sleep(0.1)
        pageToken = extractedToken[0]
        request = youtube.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=50,
            pageToken=pageToken,
            playlistId=set_id
        )
        response = request.execute()
        extractedToken = json_extract(response, "nextPageToken")  # Gets nextPageToken
        counter += 1
        print("\tFetching page " + str(counter))  # Debug
        result.append(response)  # Adds JSON response to a list of JSON responses

    return result


# MAIN PROGRAM
def backupMaker(playlistID):

    # Get API keys from file
    with open("./config.json") as f:
        keys = json.load(f)
    CLIENT_ID = keys["client_id"]
    DEVELOPER_KEY = keys["YT_devkey"]
    savePath = keys["savePath"]

    extracted = ""
    client = ""
    try:
        playlistID = int(playlistID)
        extracted = sc_get(playlistID, CLIENT_ID)
        client = "SC"
    except ValueError:
        extracted = yt_get(playlistID, DEVELOPER_KEY)
        client = "YT"

    # File saving
    fileName = savePath + client + "-" + datetime.now().strftime("%Y%m%d-%H.%M.%S") + ".json"
    with open(fileName, 'w', encoding='utf8') as outfile:
        json.dump(extracted, outfile, indent=2, ensure_ascii=False)
    sg.Popup("Saved!")
