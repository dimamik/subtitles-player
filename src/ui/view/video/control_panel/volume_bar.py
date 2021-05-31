from PyQt5.QtWidgets import QProgressBar

from resources.css_manager import CssManager


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
            CssManager.get_css_as_string(self)
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
