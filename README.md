# Smart Playlists for YouTube

A python script that runs periodically and polls given YouTube channels. Add any new videos to a provided playlist using the YouTube API. 

## Setup
Need to set up a new playlist, this script will not create a playlist. Need to set up oauth credentials for accesing the YouTube API.

### Create Playlist
In YouTube, select a video and hit the "Save" button. Choose " + Create new playlist." Give a name and choose "Unlisted" Privacy.


Hamburger Menu > Playlists and select the playlist you just created. The URL contains the playlist ID. 

`https://www.youtube.com/watch?v=VIDEO_ID&list=PLAYLIST_ID`

### Create Oauth client secrets

https://www.youtube.com/watch?v=th5_9woFJmk