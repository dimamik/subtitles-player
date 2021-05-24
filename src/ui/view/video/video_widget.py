import logging

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

from src.ui.view.video.player_wrapper import PlayerWrapper


class VideoWidget(QVideoWidget):
    """
    Playing media widget
    """

    def __init__(self, path_to_media=None):
        super(VideoWidget, self).__init__()
        self.media_player = PlayerWrapper()
        if path_to_media is None:
            logging.error("VideoWidget: path_to_media can't be empty")
            exit(-1)
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(
                path_to_media
            )))
        self.media_player.setVideoOutput(self)
        self.media_player.play()
