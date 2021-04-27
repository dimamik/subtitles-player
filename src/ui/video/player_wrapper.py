from PyQt5.QtMultimedia import QMediaPlayer


class PlayerWrapper(QMediaPlayer):
    def __init__(self):
        super(PlayerWrapper, self).__init__(None, QMediaPlayer.VideoSurface)
