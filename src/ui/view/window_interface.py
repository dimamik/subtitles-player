import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QApplication, QSizePolicy, QVBoxLayout, QHBoxLayout
from pycparser.c_ast import Enum

from resources.res_manager import ResourcesManager


def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


class WindowType(Enum):
    welcome = 0
    video = 1


class WindowInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(800, 600)

        self.setStyleSheet("""
        *{
        background: rgb(222,97,218);
        background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(158, 61, 103, 255), stop:0.509465 rgba(158, 57, 135, 255), stop:1 rgba(117, 60, 158, 255));
        }
        """)
        self.layout = QVBoxLayout()
        self.menu_box = MenuWidget(self)
        self.layout.addLayout(self.menu_box)
        self.window_type = None
        self.setWindowTitle("Subtitles Player")
        self.setWindowIcon(QIcon(ResourcesManager.get_resource('icon.png')))
        # self.showFullScreen()

    @staticmethod
    def show_itself(window):
        app = QApplication(sys.argv)
        demo = window()
        demo.show()
        sys.exit(app.exec_())


class MenuWidget(QHBoxLayout):
    def __init__(self, main_interface_instance):
        super(MenuWidget, self).__init__()
        self.addStretch(1)
        # self.setSpacing(0)
        # self.setContentsMargins(0,0,0,0)
        # self.setFixedHeight(20)
        self.main_interface_instance = main_interface_instance
        # self.button_saved = ResourcesManager.get_open_saved_button()
        self.button_open_new = ResourcesManager.get_open_new_video_button()
        self.button_open_new.clicked.connect(self.return_to_previous)
        button = ResourcesManager.get_menu_button()
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # button_saved.setContentsMargins(0,0,0,0)
        # button_open_new.setContentsMargins(0,0,0,0)

        # self.setContentMargins(0,0,0,0)

        # self.button_saved.setStyleSheet("""
        # button_saved{
        # border-style:dotted;
        # background-color: red;
        # }
        # """)

        # self.addWidget(self.button_saved, 0, Qt.AlignRight)
        self.addWidget(self.button_open_new, 0, Qt.AlignRight)
        # self.addWidget(button, 0, Qt.AlignRight)

    def return_to_previous(self):
        from src.ui.view.welcome_window import WelcomeWindow
        from src.ui.view.video.video_window import VideoWindow
        # WelcomeWindow.get_instance().show()
        print(WelcomeWindow.get_instance().window_type)
        print(VideoWindow.instance)

        if self.main_interface_instance.window_type is WindowType.welcome:
            WelcomeWindow.get_instance().hide()
            VideoWindow.get_instance().show()
        else:
            from src.ui.view.video.video_window import VideoWindow
            VideoWindow.get_instance().pause_video()
            VideoWindow.get_instance().hide()
            WelcomeWindow.get_instance().textToLearn.reload_sentences()
            WelcomeWindow.get_instance().show()
            WelcomeWindow.get_instance().menu_box.button_open_new. \
                setVisible(True)


if __name__ == '__main__':
    WindowInterface.show_itself(WindowInterface)
