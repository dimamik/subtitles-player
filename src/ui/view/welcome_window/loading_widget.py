from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QMovie
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QStyleOption, QStyle

from resources.res_manager import ResourcesManager


class LoadingWidget(QWidget):
    def __init__(self):
        """
        list_of_commands = {
        "What has been done" : is_done
        }
        """
        super(LoadingWidget, self).__init__()
        self.text_messages = QVBoxLayout()
        self.loading_process = QLabel()
        self.setStyleSheet(
            """
                        QWidget{
                    border: none;
                    z-index: 10;
                    background:none;
                    font-family: 'Raleway',sans-serif; font-size: 20px; 
                    font-weight: 800; line-height: 72px; text-align: center; text-transform: uppercase;   
                    }
            """)

        self.label = QLabel()
        self.movie = QMovie(ResourcesManager.get_loading_gif())
        self.label.setMovie(self.movie)
        self.movie.start()
        self.text_messages.addWidget(self.label, 0, Qt.AlignCenter)

        self.text_messages.addWidget(self.loading_process, 0, Qt.AlignCenter)
        self.setLayout(self.text_messages)
        self.list_of_commands = {}

    def refresh(self):
        to_print = ""
        for (str_command, is_done) in self.list_of_commands.items():
            to_print += "✅" if is_done else "❌"
            to_print += f" {str_command}\n"
        self.loading_process.setText(to_print)

    def begin_task(self, task_name):
        self.list_of_commands[task_name] = False
        self.refresh()

    def finish_task(self, task_name):
        self.list_of_commands[task_name] = True
        self.refresh()

    def clear(self):
        self.list_of_commands = {}
        self.hide()

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
