from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel

from resources.css_manager import CssManager


class FileLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("<h1>Place your file</h1>")
        self.setStyleSheet(
            CssManager.get_css_as_string(self)
        )
