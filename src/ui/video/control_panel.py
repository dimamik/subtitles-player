import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSlider, QPushButton, QApplication, QProgressBar

from src.ui.resources.res_manager import ResourcesManager
from src.ui.video.video_widget import VideoWidget


class ControlPanel(QWidget):
    def __init__(self, player_wrapper):
        super(ControlPanel, self).__init__()
        self.layout = ControlPanel.set_h_box_layout()
        self.progress_bar = ProgressBar(player_wrapper)
        self.state_button = StateButton(player_wrapper)
        self.volume_bar = VolumeBar(player_wrapper)
        self.flip_subs_button = FlipSubsButton(player_wrapper)
        self.save_subs_button = SaveSubsButton(player_wrapper)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.volume_bar)
        self.layout.addWidget(self.state_button)
        self.layout.addWidget(self.flip_subs_button)
        self.layout.addWidget(self.save_subs_button)

        self.setLayout(self.layout)

    @staticmethod
    def set_h_box_layout():
        h_box = QHBoxLayout()
        h_box.setContentsMargins(0, 0, 0, 0)
        return h_box


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


class VolumeBar(QProgressBar):
    # TODO Add round handle
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
                background-color: #666;
            }

            QProgressBar::chunk {
                background-color: black;
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


class Button(QPushButton):
    def __init__(self, icon):
        super().__init__()
        self.setFixedWidth(24)
        self.setFixedHeight(24)
        self.setIcon(icon)

        self.setIconSize(QSize(40, 50))
        self.setStyleSheet(
            """
            QPushButton{
                border: none;
                background:none;
            }
            """
        )


class StateButton(Button):
    def __init__(self, player_wrapper):
        super().__init__(ResourcesManager.get_pause_icon())
        self.media_player = player_wrapper
        self.play_status = True
        self.clicked.connect(self.change_state)

    def change_state(self):
        if self.play_status:
            self.setIcon(ResourcesManager.get_play_icon())
            self.play_status = False
            self.media_player.pause()
        else:
            self.setIcon(ResourcesManager.get_pause_icon())
            self.play_status = True
            self.media_player.play()


class FlipSubsButton(Button):
    def __init__(self, player_wrapper):
        super().__init__(ResourcesManager.get_flip_icon())
        self.media_player = player_wrapper
        self.clicked.connect(self.flip_subs)

    def flip_subs(self):
        print("Woosh I am flipping subs :D")


class SaveSubsButton(Button):
    def __init__(self, player_wrapper):
        super().__init__(ResourcesManager.get_save_icon())
        self.media_player = player_wrapper
        self.clicked.connect(self.save_subs)

    def save_subs(self):
        print("Woosh I am saving subs :D")


if __name__ == '__main__':
    app = QApplication(sys.argv)

    videoWidget = VideoWidget()

    videoplayer = ControlPanel(videoWidget)
    videoWidget.resize(640, 480)
    videoplayer.show()
    sys.exit(app.exec_())
