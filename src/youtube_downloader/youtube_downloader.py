import pytube

from resources.res_manager import ResourcesManager


class YoutubeDownloader:

    @classmethod
    def download_video(cls, youtube_url):
        youtube = pytube.YouTube(youtube_url)
        try:
            video = youtube.streams.otf(False).first()
        except Exception as ex:
            print(ex)
        video.download(ResourcesManager.get_place_to_store_yt_videos())
        print("SUCCESS ON DOWNLOAD!")
        to_ret = ResourcesManager.get_place_to_store_yt_videos() + "\\" + youtube.streams[0].default_filename
        return to_ret.replace("\\", "/")

    @classmethod
    def is_yt_link(cls, url_yt: str):
        return True if url_yt.find("https://www.youtube.com/") != -1 else False


if __name__ == '__main__':
    url = 'https://www.youtube.com/watch?v=gCYcHz2k5x0'
    print(YoutubeDownloader.download_video(url))
