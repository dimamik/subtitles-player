from PyQt5.QtWidgets import QWidget, QHBoxLayout

from src.ui.view.video.control_panel.buttons import FlipSubsButton, StateButton, SaveSubsButton
from src.ui.view.video.control_panel.progress_bar import ProgressBar
from src.ui.view.video.control_panel.volume_bar import VolumeBar


class ControlPanel(QWidget):
    def __init__(self, player_wrapper, subtitles):
        super(ControlPanel, self).__init__()
        self.layout = ControlPanel.set_h_box_layout()
        self.progress_bar = ProgressBar(player_wrapper)
        self.state_button = StateButton(player_wrapper)
        self.volume_bar = VolumeBar(player_wrapper)
        self.flip_subs_button = FlipSubsButton(player_wrapper, subtitles)
        self.save_subs_button = SaveSubsButton(player_wrapper, subtitles)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.volume_bar)
        self.layout.addWidget(self.state_button)
        self.layout.addWidget(self.flip_subs_button)
        self.layout.addWidget(self.save_subs_button)
        self.setLayout(self.layout)

    @staticmethod
    def set_h_box_layout():
        h_box = QHBoxLayout()
        h_box.setContentsMargins(0, 0, 0, 0)
        return h_box

    def pause_video(self):
        self.state_button.pause()
