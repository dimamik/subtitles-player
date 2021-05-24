from PyQt5.QtWidgets import QLabel


class ErrorLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.hide()
        self.setStyleSheet(
            """
             ErrorLabel{
                 color: red;
                 font-family: 'Raleway',sans-serif; font-size: 20px; 
                 font-weight: 800; line-height: 72px; margin: 0 0 24px; 
                 text-align: center; text-transform: uppercase;
             }
            """)

    def pop_error(self, error_message):
        self.show()
        self.setText(error_message)

    def hide_error(self):
        self.hide()
