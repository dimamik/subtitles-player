from PyQt5.QtWidgets import QProgressBar


class VolumeBar(QProgressBar):
    def __init__(self, player_wrapper):
        super().__init__()
        self.media_player = player_wrapper
        self.media_player.volumeChanged.connect(self.update_position)
        self.setTextVisible(False)
        self.setRange(0, 100)
        self.setValue(100)
        self.setFixedHeight(24)
        self.setMaximumWidth(150)
        self.dragging = False

        self.setStyleSheet(
            """
            QProgressBar {
                margin: 10px;
                height: 24px;
                border: 1px solid #555;
                border-radius: 2px;
                background-color: black;
            }

            QProgressBar::chunk {
                background-color: white;
                border-radius: 2px;
                width: 1px;
            }
            """
        )

    def update_position(self, level):
        self.setValue(level)

    def mousePressEvent(self, event):
        self.dragging = True
        value = (event.x() / self.width()) * self.maximum()
        self.media_player.setVolume(value)
        self.setValue(value)

    def mouseMoveEvent(self, event):
        if self.dragging:
            value = (event.x() / self.width()) * self.maximum()
            self.media_player.setVolume(value)
            self.setValue(value)

    def mouseReleaseEvent(self, event):
        self.dragging = False
