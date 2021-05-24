from src.ui.view.video.control_panel.control_panel import ControlPanel
from src.ui.view.video.video_widget import VideoWidget
from src.ui.view.window_interface import WindowInterface, WindowType


class VideoWindow(WindowInterface):
    instance = None

    @staticmethod
    def get_instance():
        """
        :return: Returns instance of a class if exists, else raise Exception
        """
        if VideoWindow.instance is None:
            raise Exception("This class takes parameters!")
        return VideoWindow.instance

    def __init__(self, path_to_media, subtitles):
        """
        Semi-Singleton object, returning itself with get_instance method,
        but allowing recreation
        :param path_to_media:
        :param subtitles:
        """
        VideoWindow.instance = self
        super(VideoWindow, self).__init__()
        self.controls = []
        self.video_widget = VideoWidget(path_to_media)
        self.subtitles = subtitles
        self.control_panel = ControlPanel(self.video_widget.media_player, self.subtitles)
        self.video_widget.media_player.add_event_handler(self.subtitles.update_subtitles)
        self.layout.addWidget(self.video_widget, 2)
        self.layout.addWidget(self.subtitles)
        self.layout.addWidget(self.control_panel)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.window_type = WindowType.video

    def pause_video(self):
        self.control_panel.pause_video()
