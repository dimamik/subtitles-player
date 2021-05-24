from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QMovie
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QStyleOption, QStyle

from resources.res_manager import ResourcesManager
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
        """
        list_of_commands = {
        "What has been done" : is_done
        }
        """
        super(LoadingWidget, self).__init__()
        self.text_messages = QVBoxLayout()
        self.loading_process = QLabel()
        self.setStyleSheet("""
                        QWidget{
                    border: none;
                    z-index: 10;
                    background:none;
                    font-family: 'Raleway',sans-serif; font-size: 20px; 
                    font-weight: 800; line-height: 72px; text-align: center; text-transform: uppercase;   }
                }
            """)

        self.label = QLabel()
        # self.label.setGeometry(QtCore.QRect(25, 25, 200, 200))
        # self.label.setMinimumSize(QSize(250, 250))
        # self.label.setMaximumSize(QSize(250, 250))
        # self.label.setObjectName("lb1")
        self.movie = QMovie(ResourcesManager.get_loading_gif())
        self.label.setMovie(self.movie)
        self.movie.start()
        self.text_messages.addWidget(self.label, 0, Qt.AlignCenter)

        self.text_messages.addWidget(self.loading_process, 0, Qt.AlignCenter)
        self.setLayout(self.text_messages)
        self.list_of_commands = {}

    #     TODO To Remove

    # Label Create

    def refresh(self):
        to_print = ""
        for (str_command, is_done) in self.list_of_commands.items():
            to_print += "✔" if is_done else "❌"
            to_print += str_command + "\n"
        self.loading_process.setText(to_print)
        print("Refreshed!")

    def begin_task(self, task_name):
        print("-==")
        self.list_of_commands[task_name] = False
        self.refresh()

    def finish_task(self, task_name):
        print("df")
        print(self.list_of_commands[task_name])
        self.list_of_commands[task_name] = True

        print("00")
        self.refresh()
        print("0s0")

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
        self.loadingWidget = LoadingWidget()
        self.loadingWidget.hide()
        self.layout.addWidget(self.welcomeMessage, 15, Qt.AlignTop | Qt.AlignCenter)
        self.layout.addWidget(self.flagsWidget, 15, Qt.AlignTop | Qt.AlignCenter)
        self.layout.addWidget(self.textToLearn, 15, Qt.AlignTop | Qt.AlignCenter)
        self.layout.addWidget(self.inputField, 30, Qt.AlignCenter)
        self.layout.addWidget(self.loadingWidget, 30, Qt.AlignCenter)
        self.setLayout(self.layout)
        self.output = ""
        self.file_path = ""
        self.video_window = None
        self.window_type = WindowType.welcome
        self.subtitles = None
        self.processing = False

    def dragEnterEvent(self, event):
        if not self.processing:
            event.accept()
            self.processing = True

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        url = str(event.mimeData().urls()[0].toString())
        self.inputField.hide()
        self.loadingWidget.show()

        if YoutubeDownloader.is_yt_link(url):
            # self.file_path = YoutubeDownloader.download_video(url)
            self.loadingWidget.begin_task("Downloading from youtube")
            self.welcomeWindowVM.run_thread_download_from_yt(url)
        else:
            self.loadingWidget.begin_task("Creating subtitles")
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.welcomeWindowVM.run_thread_create_subtitles(self.file_path)
        event.accept()
        self.inputField.setStyleSheet("""
                    InputField{
                border: none;
            }
        """)

    def finish_download_from_yt(self, path):
        self.file_path = path
        self.welcomeWindowVM.run_thread_create_subtitles(self.file_path)
        self.loadingWidget.finish_task("Downloading from youtube")
        self.loadingWidget.begin_task("Creating subtitles")

    def finish_create_subtitles(self, path_to_subs):
        # print(self.file_path)
        # self.video_window = VideoWindow(self.file_path, path_to_subs,
        #                                 to_lang=self.flagsWidget.flag)
        # self.video_window.show()
        # self.hide()
        self.loadingWidget.finish_task("Creating subtitles")

        self.subtitles = Subtitles(path_to_subs, to_lang=self.flagsWidget.flag)
        self.loadingWidget.begin_task("Parsing and translating subtitles")

        self.welcomeWindowVM.run_thread_parse_and_translate_subtitles(
            self.subtitles)

        # self.close()

    def finish_translate_subtitles(self, *args):
        self.loadingWidget.finish_task("Parsing and translating subtitles")
        self.loadingWidget.clear()
        # self.inputFiled.show()
        self.processing = False
        self.video_window = VideoWindow(self.file_path, self.subtitles)
        self.video_window.show()
        self.hide()
        self.close()


if __name__ == '__main__':
    WelcomeWindow.show_itself(WelcomeWindow)
