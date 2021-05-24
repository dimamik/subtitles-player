from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel


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
