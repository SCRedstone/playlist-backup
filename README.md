# Redstone's Playlist Backup Tool
Have you never noticed songs disappearing from your favourite YouTube/Soundcloud music playlists? This tool:

* Creates backups of YouTube and Soundcloud playlists
* Identifies deleted playlist contents by comparing it to your backups

#### [DOWNLOAD NOW!](https://github.com/SCRedstone/playlist-backup/releases)

## Disclaimers
Due to rate limiting issues, <b>users must provide their own YouTube and Soundcloud API keys</b> for this tool to work. This program does not store any user data except for the required API keys entered by the user.

## First-time Setup
1. Obtain the necessary YouTube and/or Soundcloud API key(s). If you don't use Soundcloud for example, you don't need to get a Soundcloud API key.
   * For YouTube API, ensure `youtube` scope is enabled.
2. Launch the program and paste the API key(s) via <b>Settings > Auth Keys</b>, then save.

## Usage Notes
* Please ensure your API quota has not been met. This prevents errors and fragmented backups.
* <b>Ensure all playlists are public/unlisted</b>, otherwise the program can't access the playlist.
* Backups save into the program's `backup` folder.

###### Latest version: v0.7.21
