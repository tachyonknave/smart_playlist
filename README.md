# Smart Playlists for YouTube

A python script that runs periodically and polls given YouTube channels. It adds any new videos to a provided playlist using the YouTube API.

## Setup
This project uses `uv` for fast package management.

1.  **Install `uv`** (if you don't have it):
    ```bash
    pipx install uv
    ```
2.  **Create and sync the environment:**
    ```bash
    uv venv
    uv pip sync requirements.txt
    ```

You also need to set up a new playlist (this script will not create one) and configure OAuth credentials for accessing the YouTube API.

### Create Playlist
In YouTube, select a video and hit the "Save" button. Choose " + Create new playlist." Give a name and choose "Unlisted" Privacy.


Hamburger Menu > Playlists and select the playlist you just created. The URL contains the playlist ID. 

`https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID`

### Create Oauth client secrets

https://www.youtube.com/watch?v=th5_9woFJmk

## Run
`yt_api/src$ uv run main.py`