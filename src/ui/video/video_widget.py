import sys

from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import QApplication

from src.ui.video.player_wrapper import PlayerWrapper


class VideoWidget(QVideoWidget):
    """
    Playing media widget
    """

    def __init__(self, path_to_media=None):
        super(VideoWidget, self).__init__()
        self.media_player = PlayerWrapper()
        if path_to_media is None:
            path_to_media = "D:\\Videos\\2021-03-24 08-01-42.mp4"
        self.media_player.setMedia(
            QMediaContent(QUrl.fromLocalFile(
                path_to_media
            )))
        self.media_player.setVideoOutput(self)
        # TODO To Remove
        self.media_player.setVolume(20)
        self.media_player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    videoplayer = VideoWidget()
    videoplayer.media_player.play()
    videoplayer.resize(640, 480)
    videoplayer.show()
    sys.exit(app.exec_())
