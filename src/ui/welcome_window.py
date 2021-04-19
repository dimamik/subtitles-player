import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QApplication

from src.sub_generator.generator import create_subtitles
from src.ui.window_interface import WindowInterface


class FileLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop File Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
            FileLabel{
            color: red;
            }
        ''')


class WelcomeWindow(WindowInterface):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        self.setAcceptDrops(True)
        self.photoViewer = FileLabel()
        mainLayout = QVBoxLayout()
        self.layout1.addWidget(self.photoViewer)

        # self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        file_path = event.mimeData().urls()[0].toLocalFile()
        if create_subtitles(file_path) is None:
            self.photoViewer.setText('\n\n GIVE NORMAL File! \n\n')
            event.ignore()

        else:
            self.photoViewer.setText('\n\n PROCESSED! \n\n')
            event.accept()

    def set_File(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))

    @staticmethod
    def show_itself(window):
        app = QApplication(sys.argv)
        demo = window()
        demo.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    WelcomeWindow.show_itself(WelcomeWindow)
