from PyQt5.QtMultimedia import QMediaPlayer


class PlayerWrapper(QMediaPlayer):
    def __init__(self):
        super(PlayerWrapper, self).__init__(None, QMediaPlayer.VideoSurface)

    def add_event_handler(self, handler_method):
        self.positionChanged.connect(handler_method)
