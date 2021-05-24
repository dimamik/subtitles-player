import os

from src.ui.view.pic_button import PicButton, QIcon


class ResourcesManager:
    dirname = os.path.dirname(__file__)

    @classmethod
    def get_icon(cls, icon_name):
        return QIcon(f"{ResourcesManager.dirname}\\buttons\\{icon_name}.png")

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
    def get_loading_gif(cls):
        return f"{ResourcesManager.dirname}\\gifs\\loading.gif"

    @classmethod
    def get_place_to_store_yt_videos(cls):
        return f"{ResourcesManager.dirname}\\downloads_youtube"

    @classmethod
    def get_return_button(cls):
        return PicButton(
            *[f"{ResourcesManager.dirname}\\buttons\\return_button.png"] * 3
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
