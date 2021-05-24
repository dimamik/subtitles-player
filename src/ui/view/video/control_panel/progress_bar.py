from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider


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
            """
            ProgressBar{
            background:none;

            }

            QSlider::sub-page:horizontal {

            background: white;

            border-radius: 0px;

            margin-top:8px;

            margin-bottom:8px;

            }

            QSlider::add-page:horizontal {

            background: black;

            border: 0px solid #777;

            border-radius: 2px;

            margin-top:8px;

            margin-bottom:8px;

            }
            QSlider::handle:horizontal {

             background-color: black;

            border: 1px solid rgba(102,102,102,102);

            border-radius: 7px;

            }
            """
        )

    def set_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        self.setValue(position)

    def duration_changed(self, duration):
        self.setRange(0, duration)
