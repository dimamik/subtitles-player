import sys

from PyQt5.QtWidgets import QApplication

from src.ui.video.control_panel import ControlPanel
from src.ui.video.subtitles import Subtitles
from src.ui.video.video_widget import VideoWidget
from src.ui.window_interface import WindowInterface


class VideoWindow(WindowInterface):
    def __init__(self, path_to_media, subtitles_path):
        super(VideoWindow, self).__init__()

        # self.v_box = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.controls = []
        self.subtitles_path = subtitles_path

        self.video_widget = VideoWidget(path_to_media)  # "D:\\Videos\\2021-03-24 08-01-42.mp4"
        self.video_widget.setStyleSheet("#video_widget{border: 10px solid;"
                                        "border-color: aqua;}")
        self.control_panel = ControlPanel(self.video_widget.media_player)

        self.subtitles = Subtitles(subtitles_path)
        self.video_widget.media_player.add_event_handler(self.subtitles.update_subtitles)
        self.layout.addWidget(self.video_widget, 2)
        self.layout.addWidget(self.subtitles)
        self.layout.addWidget(self.control_panel)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    videoplayer = VideoWindow("D:\\4_semestr\\Python\\Subtitles_Player\\Tests\\audio_samples\\small_record.wav",
                              "D:\\4_semestr\\Python\\Subtitles_Player\\res\\subtitles\\small_record-sub-2021-05-03 23-37-43.450991.txt"
                              )
    videoplayer.show()
    sys.exit(app.exec_())
