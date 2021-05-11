import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QApplication, QSizePolicy, QVBoxLayout

from resources.res_manager import ResourcesManager


class WindowInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)
        self.setStyleSheet(
            "* "
            "{background: rgb(222,97,218);"
            "background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(158, 61, 103, 255), stop:0.509465 rgba(158, 57, 135, 255), stop:1 rgba(117, 60, 158, 255));}"
            "")
        self.layout = QVBoxLayout()
        button = ResourcesManager.get_menu_button()
        self.layout.addWidget(button, 0, Qt.AlignRight | Qt.AlignTop)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.showFullScreen()

    @staticmethod
    def show_itself(window):
        app = QApplication(sys.argv)
        demo = window()
        demo.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    WindowInterface.show_itself(WindowInterface)
