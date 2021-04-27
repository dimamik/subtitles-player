import os

from src.ui.menu_button import PicButton, QIcon

dirname = os.path.dirname(__file__)


class ResourcesManager:

    @staticmethod
    def get_menu_button():
        return PicButton(f"{dirname}\\menu\\1.png", f"{dirname}\\menu\\1.png", f"{dirname}\\menu\\1.png")

    @staticmethod
    def get_play_icon():
        return QIcon(f"{dirname}\\buttons\\state_play.png")

    @staticmethod
    def get_pause_icon():
        return QIcon(f"{dirname}\\buttons\\state_pause.png")

    @staticmethod
    def get_flip_icon():
        return QIcon(f"{dirname}\\buttons\\flip_button.png")

    @staticmethod
    def get_save_icon():
        return QIcon(f"{dirname}\\buttons\\save.png")
