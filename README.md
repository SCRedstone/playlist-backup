# Redstone's Playlist Backup Tool
Have you never noticed songs disappearing from your favourite YouTube/Soundcloud music playlists? This tool:

* Creates backups of YouTube and Soundcloud playlists
* Identifies deleted playlist contents by comparing it to your backups

#### [DOWNLOAD NOW!](https://github.com/SCRedstone/playlist-backup/releases)

## First-time Setup
* Windows OS only
* Due to rate limiting issues, <b>users must provide their own YouTube and Soundcloud API keys</b>.
1. Obtain an API key for the service(s) you want to use.
   * For YouTube API, please enable the `youtube` scope.
2. Launch the program and paste the API key(s) via <b>Menu > Settings</b>, then save.

#### How to obtain playlist IDs
* <b>YouTube playlist IDs</b>: Grab the part of the playlist URL after `playlist?list=[...]`
* <b>Soundcloud playlist ID</b>: Under a playlist, click <b>Share > Embed</b> and in the Code box, look for the numbers after `api.soundcloud.com/playlists/[...]`

## Usage Notes
* Please ensure your API quota has not been met. This prevents errors and fragmented backups.
* <b>Ensure all playlists are public/unlisted</b>, otherwise the program can't access the playlist.
* By default, backups save into the program's `backup` folder.
