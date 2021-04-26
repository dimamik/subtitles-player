import sys

from PyQt5.QtWidgets import QApplication

from src.ui.video.control_panel import ControlPanel
from src.ui.video.video_widget import VideoWidget
from src.ui.window_interface import WindowInterface


class VideoWindow(WindowInterface):
    def __init__(self):
        super(VideoWindow, self).__init__()

        # self.v_box = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.controls = []
        self.video_widget = VideoWidget("D:\\Videos\\2021-03-24 08-01-42.mp4")
        self.video_widget.setStyleSheet("#video_widget{border: 10px solid;"
                                        "border-color: aqua;}")
        self.control_panel = ControlPanel(self.video_widget)
        self.layout.addWidget(self.video_widget, 2)
        self.layout.addWidget(self.control_panel)
        self.setLayout(self.layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    videoplayer = VideoWindow()
    videoplayer.show()
    sys.exit(app.exec_())
