import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QAbstractButton, QApplication


class PicButton(QAbstractButton):
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = QPixmap(pixmap)
        self.pixmap_hover = QPixmap(pixmap_hover)
        self.pixmap_pressed = QPixmap(pixmap_pressed)
        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(40, 30)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = PicButton("res/1.png", "res/1.png", "res/1.png")
    demo.show()
    sys.exit(app.exec_())
