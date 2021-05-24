import logging
from urllib.error import HTTPError

import pytube

from resources.res_manager import ResourcesManager


class YoutubeDownloader:

    @classmethod
    def download_video(cls, youtube_url):
        youtube = pytube.YouTube(youtube_url)
        video = None
        try:
            video = youtube.streams.otf(False).first()
        except HTTPError as ex:
            logging.error("YoutubeDownloader: GOOGLE Server is rejecting our requests with ex: ", ex)
            exit(-1)
        video.download(ResourcesManager.get_place_to_store_yt_videos())
        to_ret = ResourcesManager.get_place_to_store_yt_videos() + "\\" + youtube.streams[0].default_filename
        return to_ret.replace("\\", "/")

    @classmethod
    def is_yt_link(cls, url_yt: str):
        return True if url_yt.find("https://www.youtube.com/") != -1 else False
