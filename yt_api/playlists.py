import logging


def read_playlist_response(pl_response):
    playlist_page = []

    for item in pl_response['items']:
        playlist_id = item['id']
        playlist_title = item['snippet']['localized']['title']
        playlist_page.append((playlist_id, playlist_title))
        logging.debug(f"\t{playlist_id} - {playlist_title}")

    return playlist_page


def add_video_to_playlist(yt_service, playlist_id, video_id):
    request = yt_service.playlistItems().insert(
        part="id,snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": video_id,
                "position": 0
            }
        }
    )

    response = request.execute()

    # TODO check response for error


def get_playlist_item_ids_from_response(list_response):
    playlist_item_ids = []

    for item in list_response['items']:
        playlist_item_id = item['id']
        playlist_item_ids.append(playlist_item_id)

    return playlist_item_ids


def get_videos_ids_from_response(list_response):
    video_ids = []

    for item in list_response['items']:
        video_id = item['snippet']['resourceId']['videoId']
        video_ids.append(video_id)

    return video_ids


def get_videos_in_playlist(yt_service, playlist_id):
    all_videos = []

    request = yt_service.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    response = request.execute()
    vids = get_videos_ids_from_response(response)
    all_videos.extend(vids)

    while 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
        request = yt_service.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            pageToken=next_page_token,
            maxResults=50
        )
        response = request.execute()

        vids = get_videos_ids_from_response(response)
        all_videos.extend(vids)

    return all_videos


def remove_playlist_items(yt_service, playlist_item_ids):
    for playlist_item in playlist_item_ids:
        request = yt_service.playlistItems().delete(
            id=playlist_item
        )

        response = request.execute()

        # TODO check response for error


def get_items_in_playlist(yt_service, playlist_id):
    all_items = []

    request = yt_service.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    response = request.execute()
    items = get_playlist_item_ids_from_response(response)
    all_items.extend(items)

    while 'nextPageToken' in response:
        next_page_token = response['nextPageToken']
        request = yt_service.playlistItems().list(
            part="snippet",
            playlistId=playlist_id,
            pageToken=next_page_token,
            maxResults=50
        )
        response = request.execute()

        items = get_playlist_item_ids_from_response(response)
        all_items.extend(items)

    return all_items


def get_all_playlists(channel_id, youtube_service):
    playlists = []

    request = youtube_service.playlists().list(
        channelId=channel_id,
        part='snippet',
        maxResults=15
    )

    while request:
        response = request.execute()

        playlists.extend(read_playlist_response(response))

        request = youtube_service.playlists().list_next(request, response)

    return playlists
