from PyQt5.QtCore import QThread, pyqtSignal

from src.sub_generator.generator import SubtitlesGenerator
from src.ui.view_model.subtitles_vm import SubtitlesVM
from src.youtube_downloader.youtube_downloader import YoutubeDownloader


class Worker(QThread):
    output = pyqtSignal(str, name="output")  # str, "output"

    def __init__(self):
        super(Worker, self).__init__()
        self.exiting = False
        self.function = None
        self.args = []
        self.is_connected = False

    def __del__(self):
        self.exiting = True

    def render(self, func, *args):
        self.function = func
        self.args = args
        self.start()

    def run(self):
        """Long-running task"""
        res = self.function(*self.args)
        self.output.emit(res)

    def connect_output(self, finish_action):
        if self.is_connected:
            self.output.disconnect()
        self.is_connected = True
        self.output.connect(finish_action)


class WelcomeWindowVM:
    def __init__(self, view):
        self.view = view
        self.worker = Worker()

    def run_thread_create_subtitles(self, *args):
        self.worker.render(SubtitlesGenerator.create_subtitles,
                           *args)
        self.worker.connect_output(finish_action=self.view.finish_create_subtitles)

    def run_thread_parse_and_translate_subtitles(self, subtitles):
        print("I am here butts")

        subtitles_vm = SubtitlesVM(subtitles_view=subtitles)
        self.worker.render(subtitles_vm.run_parse_and_translate)
        self.worker.connect_output(finish_action=self.view.finish_translate_subtitles)

    # def run_thread_get_random_sentence(self):
    #     print("XDDD")
    #     pass

    def run_thread_download_from_yt(self, url):
        self.worker.render(YoutubeDownloader.download_video, url)
        self.worker.connect_output(finish_action=self.view.finish_download_from_yt)


if __name__ == '__main__':
    pass
