from PyQt5.QtWidgets import QWidget, QGridLayout, QGroupBox, QPushButton

from resources.css_manager import CssManager
from resources.res_manager import ResourcesManager
from src.ui.view.pic_button import QIcon, QSize


class FlagsWidget(QWidget):
    def __init__(self):
        super(FlagsWidget, self).__init__()
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        self.state_clicked = "be"
        self.setFixedWidth(440)
        self.setFixedHeight(55)

        self.setContentsMargins(0, 0, 0, 0)
        self.button_dict = {
            'be': FlagButton('be', self),
            'de': FlagButton('de', self),
            'fr': FlagButton('fr', self),
            'pl': FlagButton('pl', self),
            'ru': FlagButton('ru', self),
            'ja': FlagButton('ja', self)
        }
        self.button_dict[self.state_clicked].set()
        self.clicked_button = self.button_dict['be']

        for index, (key, val) in enumerate(self.button_dict.items()):
            layout.addWidget(val, 0, index)

        self.horizontalGroupBox.setLayout(layout)
        self.setLayout(layout)

    def country_changed(self, new_country):
        self.state_clicked = new_country
        self.clicked_button.reset()
        self.clicked_button = self.button_dict[new_country]
        self.button_dict[new_country].set()

    @property
    def flag(self):
        return self.state_clicked


class FlagButton(QPushButton):
    def __init__(self, country, flag_widget):
        super(FlagButton, self).__init__()
        self.released_path = ResourcesManager.get_flag(country)[0]
        self.pressed_path = ResourcesManager.get_flag_pressed(country)[0]
        self.country = country
        self.setIcon(QIcon(self.released_path))
        self.clicked.connect(self.on_click)
        self.flag_widget = flag_widget
        self.setCheckable(True)
        self.setStyleSheet(
            CssManager.get_css_as_string(self)
        )
        self.setIconSize(QSize(100, 150))

    def on_click(self):
        self.flag_widget.country_changed(self.country)

    def set(self):
        self.setIcon(QIcon(self.pressed_path))

    def reset(self):
        self.setIcon(QIcon(self.released_path))
