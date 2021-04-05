import sys

from PyQt5.QtWidgets import (QWidget, QGridLayout,
                             QPushButton, QApplication, QMessageBox)


def exit_app():
    QApplication.instance().quit()


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        # positions = [(i, j) for i in range(5) for j in range(4)]
        #
        # for position, name in zip(positions, names):
        #
        #     if name == '':
        #         continue
        #     button = QPushButton(name)
        grid.addWidget(QPushButton('Hello'), 2, 3)
        grid.addWidget(QPushButton('ELOO'), 1, 1, 1, 2)

        self.move(300, 150)
        self.setWindowTitle('Calculator')

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    app.setStyle("IOS")
    ex = Window()
    ex.setStyleSheet("""
        QWidget {
            background-color: rgb(255, 255, 255);
            }
        """)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
