# playlist-tool
I 'quickly' put this together to identify deleted songs/videos. It's very rough and the UX sucks, but it works.

## Functionality
* Create JSON backups of YouTube and Soundcloud Playlists
* Identify deleted songs and videos from given JSON backups

## Usage Disclaimers
You must provide your own YouTube and Soundcloud keys for this to work (no stealing my keys sry) due to rate limiting issues. It's imperative to make sure your YouTube quota hasn't been reached before running either program. Soundcloud has no quota.

## Setup
1. I used Python 3.8. This program probably works for any Python 3.x, but who knows
2. Install [Soundcloud](https://github.com/soundcloud/soundcloud-python) and [YouTube](https://developers.google.com/youtube/v3/quickstart/python) libraries
3. Obtain YouTube API credentials
   * Ensure you enable the full `youtube` scope
4. Paste your standard YouTube API key in `YT_devkey` field of `./auth/auth-keys.json`
5. Get Soundcloud credentials and fill in `client_id` of `.auth/auth-keys.json`.

## Programs
* Use `PLAYLIST_BACKUP.py` to save specified playlists as JSON files, saved in `./backup`
* Use `BACKUP-CHECKER.py` to check for deleted videos using the specified JSON playlist backup
