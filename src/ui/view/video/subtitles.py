import json
from datetime import datetime

from PyQt5.QtWidgets import QLabel

from resources.res_manager import ResourcesManager


class Subtitles(QLabel):
    def __init__(self, subs_path, to_lang='pl'):
        super(Subtitles, self).__init__()
        self.subs_path = subs_path
        self.to_lang = to_lang
        self.parseClass = None  # ParseSubtitlesJson(subs_path)
        self.translator = None  # Translator(to_lang)
        self.dictionary = None  # self.parseClass.sentences_dict
        # self.dictionary = self.translator.translate_sentences_dict(self.dictionary)
        self.show_english = False

        self.setStyleSheet("""
        Subtitles{
            font-size: 20px;
        }
        """)
        self.current_position = 0

    def check_if_position_in_range(self, new_position):
        if self.current_position < len(self.dictionary) - 1:
            next_offset = (self.dictionary[self.current_position + 1]["start"]
                           - self.dictionary[self.current_position]["end"]) / 2
        else:
            next_offset = 0
        if self.current_position > 0:
            prev_offset = (self.dictionary[self.current_position]["start"]
                           - self.dictionary[self.current_position - 1]["end"]) / 2
        else:
            prev_offset = 0
        print(prev_offset, next_offset)
        print(self.dictionary[self.current_position]["start"] + prev_offset, new_position,
              self.dictionary[self.current_position]["end"] + next_offset)
        return self.dictionary[self.current_position]["start"] + prev_offset <= new_position <= \
               self.dictionary[self.current_position]["end"] + next_offset

    def update_subtitles(self, new_position):
        new_position = float(new_position / 1000)
        if not self.check_if_position_in_range(new_position):
            subtitles = self.get_subtitles_instance(new_position)
            if not self.show_english:
                self.setText(subtitles[f"sentence_{self.to_lang}"])
            else:
                self.setText(subtitles[f"sentence"])

    def lang_changed(self):
        self.show_english = not self.show_english
        subtitles = self.dictionary[self.current_position]
        if not self.show_english:
            self.setText(subtitles[f"sentence_{self.to_lang}"])
        else:
            self.setText(subtitles[f"sentence"])

    def get_subtitles_instance(self, new_position):
        """
        Having current media position, returns subtitles to show
        :param new_position:
        :return:
        """
        if new_position > self.dictionary[self.current_position]["end"]:
            while self.current_position < len(self.dictionary) - 1 and new_position > \
                    self.dictionary[self.current_position]["end"]:
                self.current_position += 1
        else:
            while self.current_position > 0 and new_position < self.dictionary[self.current_position]["start"]:
                self.current_position -= 1
        return self.dictionary[self.current_position]

    def write_subtitles_to_file(self):
        now = datetime.now()
        to_write = {
            "date": now.strftime("%d/%m/%Y %H:%M:%S"),
            "original_sentence": self.dictionary[self.current_position]["sentence"],
            "translated_sentence": self.dictionary[self.current_position][f"sentence_{self.to_lang}"],
            "language": self.to_lang}
        with open(ResourcesManager.get_user_learned(), 'a', encoding='utf-8') as file:
            print("opened")
            file.write(json.dumps(to_write) + "\n")
        print("ended")
