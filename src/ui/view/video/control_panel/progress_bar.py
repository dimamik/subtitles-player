from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider

from resources.css_manager import CssManager


class ProgressBar(QSlider):
    def __init__(self, player_wrapper):
        super(ProgressBar, self).__init__(Qt.Horizontal)
        self.media_player = player_wrapper
        self.setRange(0, 0)
        self.setFixedHeight(24)
        self.sliderMoved.connect(self.set_position)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)
        self.setStyleSheet(
            CssManager.get_css_as_string(self)
        )

    def set_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        self.setValue(position)

    def duration_changed(self, duration):
        self.setRange(0, duration)
