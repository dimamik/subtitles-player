import os

from src.ui.view.menu_button import PicButton, QIcon

dirname = os.path.dirname(__file__)


class ResourcesManager:

    @classmethod
    def get_menu_button(cls):
        return PicButton(f"{dirname}\\menu\\1.png", f"{dirname}\\menu\\1.png", f"{dirname}\\menu\\1.png")

    @classmethod
    def get_play_icon(cls):
        return QIcon(f"{dirname}\\buttons\\state_play.png")

    @classmethod
    def get_pause_icon(cls):
        return QIcon(f"{dirname}\\buttons\\state_pause.png")

    @classmethod
    def get_flip_icon(cls):
        return QIcon(f"{dirname}\\buttons\\flip_button.png")

    @classmethod
    def get_save_icon(cls):
        return QIcon(f"{dirname}\\buttons\\save.png")

    @classmethod
    def get_resource(cls, res_name):
        return f"{dirname}\\{res_name}"

    @classmethod
    def get_flag(cls, country_shortcut):
        return (f"{dirname}\\flags\\flag_{country_shortcut}.png",
                f"{dirname}\\flags\\flag_{country_shortcut}.png",
                f"{dirname}\\flags\\flag_{country_shortcut}_selected.png")

    @classmethod
    def get_flag_pressed(cls, country_shortcut):
        return (f"{dirname}\\flags\\flag_{country_shortcut}_selected.png",
                f"{dirname}\\flags\\flag_{country_shortcut}_selected.png",
                f"{dirname}\\flags\\flag_{country_shortcut}_selected.png")
