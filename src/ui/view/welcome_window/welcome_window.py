from PyQt5.QtCore import Qt

from src.ui.view.flags_widget import FlagsWidget
from src.ui.view.learn_word_label import TextToLearn
from src.ui.view.video.subtitles import Subtitles
from src.ui.view.video.video_window import VideoWindow
from src.ui.view.welcome_window.InputField import InputField
from src.ui.view.welcome_window.lables.welcome_message_label import WelcomeMessageLabel
from src.ui.view.welcome_window.loading_widget import LoadingWidget
from src.ui.view.window_interface import WindowInterface, WindowType
from src.ui.view_model.welcome_window_vm import WelcomeWindowVM
from src.youtube_downloader.youtube_downloader import YoutubeDownloader


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
        self.welcomeMessage = WelcomeMessageLabel()
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

    def dropEvent(self, event):
        event.setDropAction(Qt.CopyAction)
        url = str(event.mimeData().urls()[0].toString())
        self.inputField.hide()
        self.loadingWidget.show()
        self.processing = True
        if YoutubeDownloader.is_yt_link(url):
            self.loadingWidget.begin_task("Downloading from youtube")
            self.welcomeWindowVM.run_thread_download_from_yt(url)
        else:
            self.loadingWidget.begin_task("Creating subtitles")
            self.file_path = event.mimeData().urls()[0].toLocalFile()
            self.welcomeWindowVM.run_thread_create_subtitles(self.file_path)
        event.accept()

    def finish_download_from_yt(self, path):
        self.file_path = path
        self.welcomeWindowVM.run_thread_create_subtitles(self.file_path)
        self.loadingWidget.finish_task("Downloading from youtube")
        self.loadingWidget.begin_task("Creating subtitles")

    def finish_create_subtitles(self, path_to_subs):
        self.loadingWidget.finish_task("Creating subtitles")

        self.subtitles = Subtitles(path_to_subs, to_lang=self.flagsWidget.flag)
        self.loadingWidget.begin_task("Parsing and translating subtitles")

        self.welcomeWindowVM.run_thread_parse_and_translate_subtitles(
            self.subtitles)

    def finish_translate_subtitles(self, *args):
        self.loadingWidget.finish_task("Parsing and translating subtitles")
        self.loadingWidget.clear()
        self.inputField.show()
        self.processing = False
        self.video_window = VideoWindow(self.file_path, self.subtitles)
        self.video_window.show()
        self.hide()
        self.close()
