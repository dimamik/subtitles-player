from PyQt5.QtWidgets import QLabel

from resources.css_manager import CssManager


class WelcomeMessageLabel(QLabel):
    def __init__(self):
        super(WelcomeMessageLabel, self).__init__()
        self.setText("Welcome in Subtitles player")
        self.setFixedHeight(25)
        self.setStyleSheet(
            CssManager.get_css_as_string(self)
        )
