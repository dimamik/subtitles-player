import os

from src.ui.view.button import PicButton, QIcon


class ResourcesManager:
    dirname = os.path.dirname(__file__)

    @classmethod
    def get_menu_button(cls):
        return PicButton(f"{ResourcesManager.dirname}\\menu\\1.png", f"{ResourcesManager.dirname}\\menu\\1.png",
                         f"{ResourcesManager.dirname}\\menu\\1.png")

    @classmethod
    def get_play_icon(cls):
        return QIcon(f"{ResourcesManager.dirname}\\buttons\\state_play.png")

    @classmethod
    def get_pause_icon(cls):
        return QIcon(f"{ResourcesManager.dirname}\\buttons\\state_pause.png")

    @classmethod
    def get_flip_icon(cls):
        return QIcon(f"{ResourcesManager.dirname}\\buttons\\flip_button.png")

    @classmethod
    def get_save_icon(cls):
        return QIcon(f"{ResourcesManager.dirname}\\buttons\\save.png")

    @classmethod
    def get_resource(cls, res_name):
        return f"{ResourcesManager.dirname}\\{res_name}"

    @classmethod
    def get_flag(cls, country_shortcut):
        return (f"{ResourcesManager.dirname}\\flags\\flag_{country_shortcut}.png",
                f"{ResourcesManager.dirname}\\flags\\flag_{country_shortcut}.png",
                f"{ResourcesManager.dirname}\\flags\\flag_{country_shortcut}_selected.png")

    @classmethod
    def get_flag_pressed(cls, country_shortcut):
        return (f"{ResourcesManager.dirname}\\flags\\flag_{country_shortcut}_selected.png",
                f"{ResourcesManager.dirname}\\flags\\flag_{country_shortcut}_selected.png",
                f"{ResourcesManager.dirname}\\flags\\flag_{country_shortcut}_selected.png")

    @classmethod
    def get_user_learned(cls):
        return f"{ResourcesManager.dirname}\\saved_subs\\saved.txt".replace("\\", "/")

    @classmethod
    def get_place_to_store_yt_videos(cls):
        return f"{ResourcesManager.dirname}\\downloads_youtube"

    @classmethod
    def get_open_new_video_button(cls):
        return PicButton(
            f"{ResourcesManager.dirname}\\buttons\\open_new.png",
            f"{ResourcesManager.dirname}\\buttons\\open_new.png",
            f"{ResourcesManager.dirname}\\buttons\\open_new.png"
        )

    @classmethod
    def get_open_saved_button(cls):
        return PicButton(
            f"{ResourcesManager.dirname}\\buttons\\saved.png",
            f"{ResourcesManager.dirname}\\buttons\\saved.png",
            f"{ResourcesManager.dirname}\\buttons\\saved.png"
        )

    @classmethod
    def read_saved_subs(cls):
        import json
        to_ret = []
        with open(f"{ResourcesManager.dirname}/saved_subs/saved.txt", "r", encoding='utf8') as file:
            lines = file.readlines()
            for line in lines:
                js = json.loads(line)
                to_ret.append(js)
        return list({v['original_sentence']: v for v in to_ret}.values())


if __name__ == '__main__':
    print(ResourcesManager.read_saved_subs())
