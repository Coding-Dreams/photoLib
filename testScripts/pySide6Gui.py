import PySide6 as pyS
from PySide6 import *
import pySide6VideoWidget as playerWidget
import time

class GUI():

    def __init__(self,processQueue,serverInitializedEvent,resultQueue):

        #initialize Queues and events
        self.processQueue=processQueue
        self.serverInitializedEvent=serverInitializedEvent
        self.resultQueue = resultQueue

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

        #define text box for server Status 
        self.serverStatus = pyS.QtWidgets.QLabel("Server Off")
        self.gridForButton.addWidget(self.serverStatus)

        #define text box for server Responses
        self.serverResponse = pyS.QtWidgets.QLabel("The following commands are: q(quit), s(save), ff(Find Face), fd(Find Date), ad(Add data)")
        self.mainGrid.addWidget(self.serverResponse,2, pyS.QtCore.Qt.AlignTop)


        #define array of Media objects
        self.mediaPlayers=[]

        self.layout = pyS.QtWidgets.QHBoxLayout(self.homeWidget)
        self.scrollArea = pyS.QtWidgets.QScrollArea(self.homeWidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = pyS.QtWidgets.QWidget()
        self.gridLayout = pyS.QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        #self.gridLayout.
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.mainGrid.addWidget(self.scrollArea,pyS.QtCore.Qt.AlignTop)


    def buttonClick(self):
        userInput = self.entry.text()
        self.entry.setText("")
        killValue=self.orderServer(userInput)
        if(killValue):
            self.window.quit()

    def addMedia(self,serverResults):
        self.mediaPlayers = []
        for i in range(0,len(serverResults)):
            if(i%2 != 0):
                self.gridLayout.setRowMinimumHeight(int(i/2),400)

            if serverResults[i].split(".")[-1]=="MP4":

                self.mediaPlayers.append(playerWidget.VideoPlayer(serverResults[i]))
                self.gridLayout.addWidget(self.mediaPlayers[-1].getWidget(),int(i/2), 0 if i%2==0 else 1)
                
            else:

                imageLabel = pyS.QtWidgets.QLabel()
                image = pyS.QtGui.QPixmap(serverResults[i].replace("\\","/"))
                image = image.scaled(400,400, pyS.QtCore.Qt.KeepAspectRatio)
                imageLabel.setPixmap(image)
                imageLabel.setMinimumSize(400, 400)
                imageLabel.setMaximumSize(400, 400)
                self.gridLayout.addWidget(imageLabel)

        self.homeWidget.show()

    def exec(self):
        self.homeWidget.show()
        self.window.exec()


    def orderServer(self,entry:str):
        guiInput = entry.split(",")
        command=guiInput[0].upper()
        serverFlag = self.serverInitializedEvent.is_set()
        if(command == ""):
            pass
        else:
            if(command=="N" and not serverFlag):
                self.processQueue.put(["N", None, None])
                time.sleep(2)
            elif(command == "O" and not serverFlag):
                try:
                    fileLocation= guiInput[1]
                    fileName = guiInput[2]
                    if(os.path.isfile(fileLocation+fileName+"-dates.pkl") and os.path.isfile(fileLocation+fileName+"-faces.pk1")):
                        self.processQueue.put(["O", fileLocation, fileName])
                        time.sleep(2)
                    self.serverResponse.setText("Successfully initalized")
                except:
                    self.serverResponse.setText("Input failed, try again!")
                    pass

            #quit function
            elif(command == "Q" and serverFlag):
                self.processQueue.put(["Q",None,None])
                return True

            #save function
            elif(command == "S" and serverFlag):
                filesaveLocation = guiInput[1]
                filesaveName = guiInput[2]
                if(os.path.exists(filesaveLocation)):
                    self.processQueue.put(["S",filesaveLocation,filesaveName])
                    self.serverResponse.setText("Save Successful")
                else:
                    self.serverResponse.setText("USER ERROR: Invalid file path")

            #Find face function
            elif(command == "FF" and serverFlag):
                userRequest = guiInput[1]
                self.processQueue.put(["FF",userRequest,None])
                result = self.resultQueue.get()
                if(result == None):
                    self.serverResponse.setText("Face not in database")
                else:
                    self.serverResponse.setText("Face Found")
                    self.addMedia(result)

            #Find date function
            elif(command == "FD" and serverFlag):
                userRequest = guiInput[1]
                self.processQueue.put(["FD",userRequest,None])
                result = self.resultQueue.get()
                if(result == None):
                    self.serverResponse.setText("Date Not in Database")
                else:
                    self.serverResponse.setText("Date Found")
                    self.addMedia(result)

            #add data
            elif(command == "AD" and serverFlag):
                self.serverResponse.setText("User Function not yet implemented, suck it lol")

            else:
                self.serverResponse.setText("Invalid command try again!")


        serverFlag = self.serverIntializedEvent.is_set()
        if(serverFlag):
            self.serverResponse.setText("Server: ON")
        else:
            self.serverResponse.setText("Server: OFF")

        

        #False as we want killValue to be false
        return False




serverGUI = GUI()
serverGUI.exec()