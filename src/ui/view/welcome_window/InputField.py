from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QStyleOption, QStyle

from src.ui.view.welcome_window.lables.error_label import ErrorLabel
from src.ui.view.welcome_window.lables.file_label import FileLabel


class InputField(QWidget):
    def __init__(self):
        super(InputField, self).__init__()
        self.error_label = ErrorLabel()
        self.file_label = FileLabel()
        self.text_messages = QVBoxLayout()
        self.setStyleSheet(
            """
                    InputField{
                border: 4px dashed black;
                z-index: 10;
            }
        """)
        self.text_messages.addWidget(self.file_label, 0, Qt.AlignCenter)
        self.text_messages.addWidget(self.error_label, 0, Qt.AlignCenter)
        self.setLayout(self.text_messages)

    def paintEvent(self, pe):
        """
        @Overrides default QWidget method
        :param pe:
        :return:
        """
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def set_error(self, error_message):
        self.error_label.pop_error(error_message)
