import PySide6 as pyS

class fullscreen(pyS.QtWidgets.QWidget):


    def __init__(self, player):
        super().__init__()

        layout = pyS.QtWidgets.QVBoxLayout()
        self.player = player
        layout.addWidget(self.player)
        self.setLayout(layout)