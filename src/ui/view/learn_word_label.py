from random import randint

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

# class LearnWordWidget(QWidget):
#     def __init__(self):
#         super(LearnWordWidget, self).__init__()
#         self.index = 0
#         self.text = TextToLearn()
#
#     def refresh(self, new_word):
#         pass
from resources.res_manager import ResourcesManager


class TextToLearn(QLabel):
    def __init__(self):
        super(TextToLearn, self).__init__()
        self.mousePressEvent = self.get_next_sentence
        self.sentences = []
        self.index = None
        self.reload_sentences()
        self.setMinimumSize(800, 130)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet('''
            TextToLearn{
            color: black;
            border-style: solid;
            text-align: center;
            border-width: 2px;
            background: #863d9e;
            padding: 20px;
            width: 200px;
            height: 150px;
            font-family: 'Raleway',sans-serif; font-size: 20px; 
            padding:0px; margin: auto;
            font-weight: 800; line-height: 72px; text-align: center; text-transform: uppercase;   }
        ''')

    def set_text(self):
        self.setText(
            self.sentences[self.index]['translated_sentence'] + "\n" +
            self.sentences[self.index]['original_sentence']
        )

    def reload_sentences(self):

        self.sentences = ResourcesManager.read_saved_subs()
        if len(self.sentences) != 0:
            self.index = randint(0, len(self.sentences) - 1)
            self.set_text()
        else:
            self.setText("Learn words by saving them")

    def get_next_sentence(self, event):
        if len(self.sentences) == 0:
            return
        self.index = (self.index + 1) % len(self.sentences)
        self.set_text()
