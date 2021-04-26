import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSlider, QPushButton, QApplication

from src.ui.resources.res_manager import ResourcesManager
from src.ui.video.video_widget import VideoWidget


class ControlPanel(QWidget):
    def __init__(self, video_widget):
        super(ControlPanel, self).__init__()
        self.layout = ControlPanel.set_h_box_layout()
        self.progress_bar = ProgressBar(video_widget.media_player)
        self.state_button = StateButton(video_widget)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.state_button)
        self.setLayout(self.layout)

    @staticmethod
    def set_h_box_layout():
        h_box = QHBoxLayout()
        h_box.setContentsMargins(0, 0, 0, 0)
        return h_box


class ProgressBar(QSlider):
    def __init__(self, media_player):
        super(ProgressBar, self).__init__(Qt.Horizontal)
        self.media_player = media_player
        self.setRange(0, 0)
        self.sliderMoved.connect(self.set_position)
        self.media_player.positionChanged.connect(self.position_changed)
        self.media_player.durationChanged.connect(self.duration_changed)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def position_changed(self, position):
        self.setValue(position)

    def duration_changed(self, duration):
        self.setRange(0, duration)


class StateButton(QPushButton):
    def __init__(self, video_widget):
        super().__init__()
        self.video_widget = video_widget
        # self.setEnabled(False)  # ?
        self.play_status = True
        self.setIcon(ResourcesManager.get_pause_icon())
        self.clicked.connect(self.change_state)
        self.setFixedWidth(24)
        self.setFixedHeight(24)
        self.setIconSize(QSize(40, 50))

    def change_state(self):
        if self.play_status:
            self.setIcon(ResourcesManager.get_play_icon())
            self.play_status = False
            self.video_widget.pause()
        else:
            self.setIcon(ResourcesManager.get_pause_icon())
            self.play_status = True
            self.video_widget.play()


class VolumeBar(QWidget):
    pass


class FlipSubsButton(QWidget):
    pass


class SaveSubsButton(QWidget):
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    videoWidget = VideoWidget()

    videoplayer = ControlPanel(videoWidget)
    videoWidget.resize(640, 480)
    videoplayer.show()
    sys.exit(app.exec_())
