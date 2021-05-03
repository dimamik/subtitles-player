from PyQt5.QtWidgets import QLabel

from src.translation.prep_translation import ParseSubtitlesJson
from src.translation.translation import Translator


class Subtitles(QLabel):
    def __init__(self, subs_path):
        super(Subtitles, self).__init__()
        self.subs_path = subs_path
        self.parseClass = ParseSubtitlesJson(subs_path)
        self.dictionary = self.parseClass.sentences_dict
        self.translator = Translator(to_lang='pl')
        self.dictionary = self.translator.translate_dict(self.dictionary, "sentence")
        print(len(self.dictionary))
        self.setStyleSheet("""
        Subtitles{
            font-size: 20px;
        }
        """)
        self.current_position = 0

    def check_if_position_in_range(self, new_position):
        print("starting")
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
        print("ending")
        print(prev_offset, next_offset)
        print(self.dictionary[self.current_position]["start"] + prev_offset, new_position,
              self.dictionary[self.current_position]["end"] + next_offset)
        return self.dictionary[self.current_position]["start"] + prev_offset <= new_position <= \
               self.dictionary[self.current_position]["end"] + next_offset

    def update_subtitles(self, new_position):
        print(self.dictionary)
        print("o")
        new_position = float(new_position / 1000)
        if not self.check_if_position_in_range(new_position):
            print("here")
            subtitles = self.get_subtitles_instance(new_position)
            # TODO Add var to flip subs and select language
            self.setText(subtitles["sentence_pl"])

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

        # while self.current_position > 0 and sec_time < self.dictionary[self.current_position]["start"]:
        #    self.current_position -= 1
        # return self.dictionary[self.current_position]
