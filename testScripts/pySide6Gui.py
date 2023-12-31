import PySide6 as pyS
from PySide6 import *
import pySide6VideoWidget as playerWidget

class GUI():

    def __init__(self):
        #define window
        self.window = pyS.QtWidgets.QApplication()

        #define homeWidget
        self.homeWidget = pyS.QtWidgets.QWidget()
        self.homeWidget.setMinimumSize(860, 800)
        self.homeWidget.setMaximumSize(860, 800)

        self.mainGrid = pyS.QtWidgets.QBoxLayout(pyS.QtWidgets.QBoxLayout.TopToBottom, self.homeWidget)

        #define grid for entry and button
        self.gridForButton = pyS.QtWidgets.QBoxLayout(pyS.QtWidgets.QBoxLayout.LeftToRight)
        self.mainGrid.addLayout(self.gridForButton)

        #define userEntry box
        self.entry = pyS.QtWidgets.QLineEdit()

        self.gridForButton.addWidget(self.entry,2)

        #define Button
        self.button = pyS.QtWidgets.QPushButton("Send Command")
        self.button.clicked.connect(self.buttonClick)
        self.gridForButton.addWidget(self.button,1)


        #define array of Media objects
        self.mediaPlayers=[]

        self.layout = pyS.QtWidgets.QHBoxLayout(self.homeWidget)
        self.scrollArea = pyS.QtWidgets.QScrollArea(self.homeWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = pyS.QtWidgets.QWidget()
        self.gridLayout = pyS.QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        #self.gridLayout.
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.mainGrid.addWidget(self.scrollArea)


    def buttonClick(self):
        userInput = self.entry.text()
        self.entry.setText("")
        print(userInput)
        serverResults = ["D:\\converted\\1900\\01\\01\\1400.MP4","D:\\converted\\1900\\01\\01\\11.MP4","D:\\converted\\1900\\01\\01\\12.MP4","D:\\converted\\1900\\01\\01\\12.MP4","D:\\converted\\1900\\01\\01\\12.MP4","D:\\converted\\1900\\01\\01\\12.MP4"]
        self.mediaPlayers = []
        for i in range(0,len(serverResults)):
            if(i%2 != 0):
                self.gridLayout.setRowMinimumHeight(int(i/2),400)

            if serverResults[i].split(".")[-1]=="MP4":

                self.mediaPlayers.append(playerWidget.VideoPlayer(serverResults[i]))
                self.gridLayout.addWidget(self.mediaPlayers[-1].getWidget(),int(i/2), 0 if i%2==0 else 1)
                
            else:
                pass

        self.homeWidget.show()

    def exec(self):
        self.homeWidget.show()
        self.window.exec()




serverGUI = GUI()
serverGUI.exec()