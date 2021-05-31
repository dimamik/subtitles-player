from random import randint

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from resources.css_manager import CssManager
from resources.res_manager import ResourcesManager


class TextToLearn(QLabel):
    def __init__(self):
        super(TextToLearn, self).__init__()
        self.mousePressEvent = self.get_next_sentence
        self.sentences = [{}]
        self.index = None
        self.reload_sentences()
        self.setMinimumSize(800, 130)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            CssManager.get_css_as_string(self)
        )

    def set_text(self):
        self.setText(
            f"{self.sentences[self.index]['translated_sentence']}\n"
            f"{self.sentences[self.index]['original_sentence']}"
        )

    def reload_sentences(self):

        self.sentences = ResourcesManager.read_saved_subs()
        if len(self.sentences) != 0:
            self.index = randint(0, len(self.sentences) - 1)
            self.set_text()
        else:
            self.setText("Learn words by saving them")

    # noinspection PyUnusedLocal
    def get_next_sentence(self, event):
        if len(self.sentences) == 0:
            return
        self.index = (self.index + 1) % len(self.sentences)
        self.set_text()
