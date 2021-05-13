import sys

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QApplication, QWidget, QStyleOption, QStyle

from src.sub_generator.generator import SubtitlesGenerator
from src.ui.view.flags_widget import FlagsWidget
from src.ui.view.video.video_window import VideoWindow
from src.ui.view.window_interface import WindowInterface, WindowType
from src.youtube_downloader.youtube_downloader import YoutubeDownloader


class FileLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setAlignment(Qt.AlignCenter)
        self.setText("<h1>Place your file</h1>")
        self.setStyleSheet('''

            FileLabel{
            color: black;
              font-family: 'Raleway',sans-serif; font-size: 25px; 
              font-weight: 800; line-height: 72px; margin: 0 0 24px; text-align: center; text-transform: uppercase;   }
        ''')


class ErrorLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.hide()
        self.setStyleSheet('''
                   ErrorLabel{
                   color: red;
                     font-family: 'Raleway',sans-serif; font-size: 20px; 
                     font-weight: 800; line-height: 72px; margin: 0 0 24px; 
                     text-align: center; text-transform: uppercase;}

               ''')

    def pop_error(self, error_message):
        self.show()
        self.setText(error_message)

    def hide_error(self):
        self.hide()


class LoadingWidget(QWidget):
    def __init__(self):
        super(LoadingWidget, self).__init__()
        pass


class WelcomeMessage(QLabel):
    def __init__(self):
        super(WelcomeMessage, self).__init__()
        self.setText("Welcome in Subtitles player\nPlace your file or a link in section below")

        self.setStyleSheet('''
            WelcomeMessage{
            color: black;
              font-family: 'Raleway',sans-serif; font-size: 30px; 
             padding:0; margin: auto;
              font-weight: 800; line-height: 72px; text-align: center; text-transform: uppercase;   }
        ''')


class InputField(QWidget):
    def __init__(self):
        super(InputField, self).__init__()
        self.error_label = ErrorLabel()
        self.file_label = FileLabel()
        self.text_messages = QVBoxLayout()
        self.setStyleSheet("""
                    InputField{
                border: 4px dashed black;
                z-index: 10;
            }
        """)
        self.text_messages.addWidget(self.file_label, 0, Qt.AlignCenter)
        self.text_messages.addWidget(self.error_label, 0, Qt.AlignCenter)
        self.setLayout(self.text_messages)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)


class Worker(QThread):
    output = pyqtSignal(str, name="output")

    def __init__(self):
        super(Worker, self).__init__()
        self.exiting = False
        self.path = ""

    def __del__(self):
        self.exiting = True

    def render(self, path):
        self.path = path
        self.start()

    def run(self):
        """Long-running task."""
        # TODO Warning USING LOGIC IN VIEW!
        res = SubtitlesGenerator.create_subtitles(self.path)
        self.output.emit(res)


class WelcomeWindow(WindowInterface):
    __instance = None

    @staticmethod
    def get_instance():
        """ Static access method. """
        if WelcomeWindow.__instance is None:
            WelcomeWindow()
        return WelcomeWindow.__instance

    def __init__(self):
        if WelcomeWindow.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            WelcomeWindow.__instance = self
        super(WelcomeWindow, self).__init__()
        self.setAcceptDrops(True)
        self.inputField = InputField()
        self.welcomeMessage = WelcomeMessage()
        self.flagsWidget = FlagsWidget()

        self.thread = Worker()
        # self.textLabel = FileLabel()
        self.layout.addWidget(self.welcomeMessage, 15, Qt.AlignTop)
        self.layout.addWidget(self.flagsWidget)
        self.layout.addWidget(self.inputField, 30, Qt.AlignCenter)
        self.setLayout(self.layout)
        self.output = ""
        self.file_path = ""
        self.video_window = None
        self.window_type = WindowType.welcome

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        url = str(event.mimeData().urls()[0].toString())

        if YoutubeDownloader.is_yt_link(url):
            print("yt")
            print(url)
            self.file_path = YoutubeDownloader.download_video(url)
        else:
            print("not_yt")
            self.file_path = event.mimeData().urls()[0].toLocalFile()
        print(self.file_path)
        self.thread.render(self.file_path)
        self.thread.output.connect(self.thread_finished)
        event.accept()

    def thread_finished(self, arg):
        print(self.file_path)
        self.video_window = VideoWindow(self.file_path, arg,
                                        to_lang=self.flagsWidget.flag)
        self.video_window.show()
        self.hide()
        # self.close()

    @staticmethod
    def show_itself(window):
        app = QApplication(sys.argv)
        demo = window()
        demo.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    WelcomeWindow.show_itself(WelcomeWindow)
