''' BACKUP CHECKER uses pre-made backup json files to check and identify deleted YT/SC songs in a playlist '''

import json
import PySimpleGUI as sg
from utils.errorPopupUtil import error
from utils.playlistGetUtil import sc_get, yt_get


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

    # Extract metadata from local backup
    username_local, song_local, songID_local, playlistID_local, title = [], [], [], "", "<PLAYLIST NAME>"
    songID_new = []  # Stores newly retrieved song IDs
    try:
        username_local, song_local, songID_local, playlistID_local = yt_extract(playlistData)
        clientType = "YT"
    except:
        username_local, song_local, songID_local, playlistID_local = sc_extract(playlistData)
        clientType = "SC"

    # Extract metadata from online playlist
    if clientType == "YT":
        if DEVELOPER_KEY == "":
            error("YouTube API key is missing! Please check your settings.")
            return
        extracted, title = yt_get(playlistID_local, DEVELOPER_KEY)
        x, y, songID_new, z = yt_extract(extracted)  # Only need song ID
    elif clientType == "SC":
        if CLIENT_ID == "":
            error("Soundcloud API key is missing! Please check your settings.")
            return
        extracted, title = sc_get(playlistID_local, CLIENT_ID)
        x, y, songID_new, z = sc_extract(extracted)  # Only need song ID

    # Removes IDs found online if there are songs that were removed
    for i in songID_new:
        if i in songID_local:  # If ID is in both local and online, remove from both
            index = songID_local.index(i)
            songID_local.remove(i)
            username_local.pop(index)
            song_local.pop(index)

    # PySimpleGUI output
    if len(songID_local) > 0:
        layout = [[sg.Text(str(len(songID_local)) + " songs removed from playlist " + title + ": ")],
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
        sg.popup("No missing songs found in " + title +
                 "!\nIt might be a good idea to make a new backup, especially if new songs have been added since.",
                 title="Result")
