from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QStyleOption, QStyle

from src.ui.view.flags_widget import FlagsWidget
from src.ui.view.learn_word_label import TextToLearn
from src.ui.view.video.subtitles import Subtitles
from src.ui.view.video.video_window import VideoWindow
from src.ui.view.window_interface import WindowInterface, WindowType
from src.ui.view_model.welcome_window_vm import WelcomeWindowVM
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
        pass  # TODO


class WelcomeMessage(QLabel):
    def __init__(self):
        super(WelcomeMessage, self).__init__()
        self.setText("Welcome in Subtitles player")
        self.setFixedHeight(25)
        self.setStyleSheet('''
            WelcomeMessage{
            color: black;
            text-align: center;
            font-family: 'Raleway',sans-serif; font-size: 30px; 
            padding:0px; margin: auto;
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
        self.menu_box.button_open_new.setVisible(False)
        self.inputField = InputField()
        self.welcomeMessage = WelcomeMessage()
        self.flagsWidget = FlagsWidget()
        self.textToLearn = TextToLearn()
        self.welcomeWindowVM = WelcomeWindowVM(self)
        self.layout.addWidget(self.welcomeMessage, 15, Qt.AlignTop | Qt.AlignCenter)
        self.layout.addWidget(self.flagsWidget, 15, Qt.AlignTop | Qt.AlignCenter)
        self.layout.addWidget(self.textToLearn, 15, Qt.AlignTop | Qt.AlignCenter)
        self.layout.addWidget(self.inputField, 30, Qt.AlignCenter)
        self.setLayout(self.layout)
        self.output = ""
        # self.setStyleSheet("""
        # WelcomeWindow{
        #     margin:0;
        # }
        # """)
        self.file_path = ""
        self.video_window = None
        self.window_type = WindowType.welcome
        self.subtitles = None

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        url = str(event.mimeData().urls()[0].toString())

        if YoutubeDownloader.is_yt_link(url):
            # self.file_path = YoutubeDownloader.download_video(url)
            self.welcomeWindowVM.run_thread_download_from_yt(url)
        else:
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.welcomeWindowVM.run_thread_create_subtitles(self.file_path)
        event.accept()

    def finish_download_from_yt(self, path):
        self.file_path = path
        self.welcomeWindowVM.run_thread_create_subtitles(self.file_path)

    def finish_create_subtitles(self, path_to_subs):
        print(self.file_path)
        # self.video_window = VideoWindow(self.file_path, path_to_subs,
        #                                 to_lang=self.flagsWidget.flag)
        # self.video_window.show()
        # self.hide()
        self.subtitles = Subtitles(path_to_subs, to_lang=self.flagsWidget.flag)
        self.welcomeWindowVM.run_thread_parse_and_translate_subtitles(
            self.subtitles)

        # self.close()

    def finish_translate_subtitles(self, *args):
        self.video_window = VideoWindow(self.file_path, self.subtitles)
        self.video_window.show()
        self.hide()
        self.close()

    # @staticmethod
    # def show_itself(window):
    #     app = QApplication(sys.argv)
    #     demo = window()
    #     demo.show()
    #     sys.exit(app.exec_())


if __name__ == '__main__':
    # loggerConfig('mystring.log')
    WelcomeWindow.show_itself(WelcomeWindow)
