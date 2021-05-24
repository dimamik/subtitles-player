from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QPushButton

from resources.res_manager import ResourcesManager


class Button(QPushButton):
    def __init__(self, icon):
        super().__init__()
        self.setFixedWidth(35)
        self.setFixedHeight(45)
        self.setIcon(icon)

        self.setIconSize(QSize(35, 45))
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
        super().__init__(ResourcesManager.get_icon("state_pause"))
        self.media_player = player_wrapper
        self.play_status = True
        self.clicked.connect(self.change_state)

    def change_state(self):
        if self.play_status:
            self.pause()
        else:
            self.play()

    def pause(self):
        self.setIcon(ResourcesManager.get_icon("state_play"))
        self.play_status = False
        self.media_player.pause()

    def play(self):
        self.setIcon(ResourcesManager.get_icon("state_pause"))
        self.play_status = True
        self.media_player.play()


class FlipSubsButton(Button):
    def __init__(self, player_wrapper, subtitles):
        super().__init__(ResourcesManager.get_icon("flip_button"))
        self.media_player = player_wrapper
        self.subtitles = subtitles
        self.clicked.connect(self.flip_subs)
        self.setMouseTracking(True)
        self.installEventFilter(self)

    def eventFilter(self, object, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.setIcon(ResourcesManager.get_icon("flip_button_red"))
            self.flip_subs()
            return True

        elif event.type() == QtCore.QEvent.Leave:
            self.setIcon(ResourcesManager.get_icon("flip_button"))
            return True

        return False

    def flip_subs(self):
        self.subtitles.lang_changed()


class SaveSubsButton(Button):
    def __init__(self, player_wrapper, subtitles):
        super().__init__(ResourcesManager.get_icon("save"))
        self.subtitles = subtitles
        self.media_player = player_wrapper
        self.clicked.connect(self.save_subs)
        self.setMouseTracking(True)
        self.installEventFilter(self)

    def eventFilter(self, _, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.setIcon(ResourcesManager.get_icon("save_button_red"))
            self.save_subs()
            return True

        elif event.type() == QtCore.QEvent.Leave:
            self.setIcon(ResourcesManager.get_icon("save"))
            return True

        return False

    def save_subs(self):
        self.subtitles.write_subtitles_to_file()
