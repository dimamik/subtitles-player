import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout

from src.sub_generator.generator import create_subtitles


class FileLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop File Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
            *{
            color: red;
            }
        ''')


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.setAcceptDrops(True)

        mainLayout = QVBoxLayout()
        self.photoViewer = FileLabel()
        mainLayout.addWidget(self.photoViewer)

        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        event.accept()

    # def dragMoveEvent(self, event):
    #     if event.mimeData().hasFile:
    #         event.accept()
    #     else:
    #         event.ignore()

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


app = QApplication(sys.argv)
demo = AppDemo()
demo.show()
sys.exit(app.exec_())
