from PyQt5.QtWidgets import QLabel


class WelcomeMessageLabel(QLabel):
    def __init__(self):
        super(WelcomeMessageLabel, self).__init__()
        self.setText("Welcome in Subtitles player")
        self.setFixedHeight(25)
        self.setStyleSheet(
            """ 
                WelcomeMessageLabel{
                color: black;
                background:none;
                text-align: center;
                font-family: 'Raleway',sans-serif; font-size: 30px; 
                padding:0px; margin: auto;
                font-weight: 800; line-height: 72px; text-align: center; text-transform: uppercase;   
                }
                
            """
        )
