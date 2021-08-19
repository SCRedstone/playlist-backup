''' Functions that return playlist responses from YouTube and Soundcloud APIs '''

import json
import os
import urllib.request
from time import sleep
import googleapiclient.discovery
import googleapiclient.errors
from utils.extract import json_extract
import requests


def sc_get(set_id, CLIENT_ID):
    with urllib.request.urlopen("https://api.soundcloud.com/playlists/" + str(set_id) + "?client_id=" + CLIENT_ID) as url:
        playlist = json.loads(url.read().decode())

    title = '"' + playlist["title"] + '"'  # Extract playlist name from response
    return playlist, title


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
        sleep(0.1)  # Rate limiter
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

    title = '"' + requests.get("https://www.googleapis.com/youtube/v3/playlists?part=snippet%2Clocalizations&id=" +
                               str(set_id) + "&fields=items(localizations%2Csnippet%2Flocalized%2Ftitle)&key=" +
                               DEVELOPER_KEY).json()["items"][0]["snippet"]["localized"]["title"] + '"'  # Playlist name
    return result, title
