''' BACKUP CHECKER uses pre-made backup json files to check and identify deleted YT/SC songs in a playlist '''

import json
import os
import time
import urllib.request
import PySimpleGUI as sg
import googleapiclient.discovery
import googleapiclient.errors
import requests
from utils.errorPopupUtil import error
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


def yt_extract(data):
    song_id, song, artist, playlist_id = [], [], [], []
    for y in data:
        for x in y["items"]:
            if not (x["snippet"]["title"] == "Deleted video" or x["snippet"]["title"] == "Private video"):  # Ignores deleted/private videos
                song_id.append(x["contentDetails"]["videoId"])
                song.append(x["snippet"]["title"])
                artist.append(x["snippet"]["videoOwnerChannelTitle"])
                playlist_id.append(x["snippet"]["playlistId"])  # playlist_id gets filled with the same thing

    return artist, song, song_id, playlist_id[0]


def sc_extract(data):
    # Iterates through 'track' array to get all track IDs
    sc_id, artists, songs = [], [], []
    for x in data["tracks"]:
        sc_id.append(x["id"])
        songs.append(x["title"])
        artists.append(x["user"]["username"])
    return artists, songs, sc_id, str(data["id"])


# MAIN FUNCTION
def backupChecker(playlistData):

    # Get API keys from file
    with open("./config.json") as f:
        keys = json.load(f)
    CLIENT_ID = keys["client_id"]
    DEVELOPER_KEY = keys["YT_devkey"]

    username_local, song_local, songID_local, playlistID_local, title = [], [], [], "", "<PLAYLIST NAME>"
    songID_new = []  # Stores newly retrieved song IDs
    try:
        username_local, song_local, songID_local, playlistID_local = yt_extract(playlistData)
        clientType = "YT"
    except:
        username_local, song_local, songID_local, playlistID_local = sc_extract(playlistData)
        clientType = "SC"

    # Extracts IDs from local playlist
    if clientType == "YT":
        if DEVELOPER_KEY == "":
            error("YouTube API key is missing! Please check your settings.")
            return
        extracted = yt_get(playlistID_local, DEVELOPER_KEY)
        x, y, songID_new, z = yt_extract(extracted)  # Only need song ID
        title = requests.get("https://www.googleapis.com/youtube/v3/playlists?part=snippet%2Clocalizations&id=" +
                             str(playlistID_local) + "&fields=items(localizations%2Csnippet%2Flocalized%2Ftitle)&key=" +
                             DEVELOPER_KEY).json()["items"][0]["snippet"]["localized"]["title"]  # Grabs playlist name
    elif clientType == "SC":
        if CLIENT_ID == "":
            error("Soundcloud API key is missing! Please check your settings.")
            return
        extracted = sc_get(playlistID_local, CLIENT_ID)
        x, y, songID_new, z = sc_extract(extracted)  # Only need song ID
        title = extracted["title"]  # Extract playlist name

    # Removes IDs found online if there are songs that were removed
    for i in songID_new:
        if i in songID_local:  # If ID is in both local and online, remove ID from both
            index = songID_local.index(i)
            songID_local.remove(i)
            username_local.pop(index)
            song_local.pop(index)

    # PySimpleGUI output
    if len(songID_local) > 0:
        layout = [[sg.Text(str(len(songID_local)) + ' songs removed from playlist "' + title + '": ')],
                  [sg.Multiline(size=(55, 9), key="output")],
                  [sg.OK()]]
        window = sg.Window('Result', layout, modal=True, finalize=True)

        # Organize Multiline output
        for x in range(len(songID_local)):
            window['output'].print(songID_local[x])
            window['output'].print("\t" + str(username_local[x]) + " - " + str(song_local[x]))
        while True:
            event, value = window.Read()
            if event == 'OK' or event == sg.WIN_CLOSED:
                break
        window.close()

    else:
        sg.popup("No missing songs found! It might be a good idea to make a new backup.", title="Result")
