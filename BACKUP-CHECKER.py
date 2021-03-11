# BACKUP CHECKER uses pre-made backup json files to check and identify deleted YT/SC songs in a playlist
import os
import googleapiclient.discovery
import googleapiclient.errors
import json
import time
from utils.extract import json_extract
import urllib.request

# Get API keys from file
with open("auth/auth-keys.json") as f:
    keys = json.load(f)
CLIENT_ID = keys["client_id"]
DEVELOPER_KEY = keys["YT_devkey"]


def sc_get(set_id):
    with urllib.request.urlopen("https://api.soundcloud.com/playlists/" + str(set_id) + "?client_id=" + CLIENT_ID) as url:
        playlist = json.loads(url.read().decode())
    return playlist


def yt_get(set_id):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)
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
        print("\tFetching page " + str(counter))
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


print("NOTE: Please ensure the relevant playlists are PUBLIC so the program has access.")
while True:
    try:
        filename = input("Enter the backup file's name (___.json): ")
        with open('backup/'+filename+'.json', encoding='utf-8') as f:
            playlistData = json.load(f)
        break
    except Exception as e:
        print(e)

username_local, song_local, songID_local, playlistID_local = [], [], [], ""
songID_new = []  # Stores newly retrieved song IDs
try:
    username_local, song_local, songID_local, playlistID_local = yt_extract(playlistData)
    clientType = "YT"
except:
    username_local, song_local, songID_local, playlistID_local = sc_extract(playlistData)
    clientType = "SC"

field = input("Enter a live playlist ID to compare between (nothing to continue with the same playlist): ")
if field != "":
    playlistID_local = field

if clientType == "YT":
    extracted = yt_get(playlistID_local)
    x, y, songID_new, z = yt_extract(extracted)  # Only need song ID
elif clientType == "SC":
    extracted = sc_get(playlistID_local)
    x, y, songID_new, z = sc_extract(extracted)  # Only need song ID
else:
    print("Major error.")

# Removes IDs found online if there are songs that were removed
for i in songID_new:
    if i in songID_local:
        index = songID_local.index(i)
        songID_local.remove(i)
        username_local.pop(index)
        song_local.pop(index)

if len(songID_local) > 0:
    print("\n" + str(len(songID_local)) + " songs removed from your playlist: ")
    for x in range(len(songID_local)):
        print(songID_local[x])
        print("\t" + str(username_local[x]) + " - " + str(song_local[x]))
else:
    print("\nNo missing songs found! Might be a good idea to make a new backup.")
