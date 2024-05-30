from time import sleep

from googleapiclient.discovery import build

from yt_api.channel_videos import get_channel_videos
from yt_api.config import Config
from yt_api.credentials import get_credentials
from yt_api.playlists import add_video_to_playlist, get_videos_in_playlist

import logging


def update_playlist(playlist_config):
    credentials = get_credentials()

    youtube_service = build('youtube', 'v3', credentials=credentials)

    channel_list = playlist_config.get_channel_list()

    all_videos = []

    for channel in channel_list:
        all_videos.extend(get_channel_videos(youtube_service, channel))

    target_playlist_id = playlist_config.get_target_playlist()

    playlist_video_ids = get_videos_in_playlist(youtube_service, target_playlist_id)

    sorted_videos = sorted(all_videos, key=lambda video: video.published_at)

    added_videos = playlist_video_ids.copy()
    for vid in sorted_videos:
        video_resource_id = vid.resourceId['videoId']
        if video_resource_id not in added_videos:
            logging.info(f"Adding video: {vid.title}")
            add_video_to_playlist(youtube_service, target_playlist_id, vid.resourceId)
            added_videos.append(video_resource_id)
    logging.info("Done adding videos")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    config = Config()
    config.load_config()

    sleep_time = config.get_sleep_time()

    while True:
        update_playlist(config)
        logging.info("Sleeping...")
        sleep(sleep_time)
