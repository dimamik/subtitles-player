from PyQt5.QtWidgets import QLabel

from resources.css_manager import CssManager


class ErrorLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.hide()

        self.setStyleSheet(
            CssManager.get_css_as_string(self)
        )

    def pop_error(self, error_message):
        self.show()
        self.setText(error_message)

    def hide_error(self):
        self.hide()
