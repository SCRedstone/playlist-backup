# Redstone's Playlist Backup Tool
Ever noticed songs disappearing from your favourite playlists without you knowing what they were? This tool:

* Creates backups of YouTube and Soundcloud playlists
* Identifies deleted playlist contents by comparing it to backups

#### [DOWNLOAD NOW!](https://github.com/SCRedstone/playlist-backup/releases)

## First-time Setup
* Due to rate limiting issues, **users must provide their own YouTube and/or Soundcloud API keys**.
1. Obtain an API key for the service(s) you want to use.
   * For YouTube API, please enable at least the `youtube` scope.
2. Launch the program, paste the API key(s) via **Menu > Settings**, then save.

#### How to obtain playlist IDs
* **YouTube playlist IDs**: Grab the part of the playlist URL in `/playlist?list=[...]`
* **Soundcloud playlist ID**: Under a playlist, click <b>Share > Embed</b> and in the Code box, look for the numbers in `api.soundcloud.com/playlists/[...]`

## Usage Notes
* Windows OS only, or simply download this repo, install all dependencies, and run `main.py`.
* **Ensure all playlists are public/unlisted**, otherwise the program has no access.
* Please ensure your API quota has not been met. This prevents errors and fragmented backups.
* **Keep `config.json` safe**!! API keys are saved as **plain text** into `config.json` within the root folder. Meanwhile, backups save into the program's `backup` folder by default.
* This program cannot catch YouTube videos that have been georestricted in your region, showing up as 'unavailable videos' in playlists. <strike>To identify such songs: play a playlist, press **CTRL+F**, and type `video blocked in country`. Georestricted videos should be highlighted in the playlist side-menu.</strike> This feature has been removed at this time. At the moment, you can only find the number of georestricted videos: Play a playlist and scroll to the bottom where it should say 'X unavailable videos are hidden'.

## Screenshots
![Main menu](https://i.imgur.com/t0uwnje.png "Main menu")
![Results window](https://i.imgur.com/op84Dj7.png "Results window")
