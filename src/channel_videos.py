from model.video_item import VideoItem


def get_channel_videos(youtube_service, channel_name=""):
    vid_array = []

    if channel_name[0] == '@':
        request = youtube_service.channels().list(
            part='contentDetails',
            forHandle=channel_name[1:]
        )
    else:
        request = youtube_service.channels().list(
            part='contentDetails',
            forUsername=channel_name
        )

    response = request.execute()
    uploads_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    request = youtube_service.playlistItems().list(
        playlistId=uploads_id,
        part='snippet',
        maxResults=15
    )

    response = request.execute()

    for item in response['items']:
        vid = VideoItem(item['snippet']['title'])
        vid.resourceId = item['snippet']['resourceId']
        vid.published_at = item['snippet']['publishedAt']
        vid_array.append(vid)

    return vid_array
