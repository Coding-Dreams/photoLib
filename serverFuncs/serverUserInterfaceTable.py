import PySide6 as pyS
from PySide6 import *
import pySide6VideoWidget as playerWidget
import time
import os
import math
#import multiprocessing as mp

class GUI():

    def __init__(self,processQueue,serverInitializedEvent,resultQueue):

        self.NUMROWS = 3

        #initialize Queues and events
        self.processQueue=processQueue
        self.serverInitializedEvent=serverInitializedEvent
        self.resultQueue = resultQueue

        #define window
        self.window = pyS.QtWidgets.QApplication()

        #define homeWidget
        self.homeWidget = pyS.QtWidgets.QWidget()
        self.homeWidget.setMinimumSize(1260, 800)
        self.homeWidget.setMaximumSize(1260, 800)

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

        self.initScrollArea(1)

    def initScrollArea(self,numRows):
        self.gridTable = pyS.QtWidgets.QTableWidget(numRows,self.NUMROWS,self.homeWidget)
        header = self.gridTable.horizontalHeader()
        header.setMinimumSectionSize(400)
        footer = self.gridTable.verticalHeader()
        footer.setMinimumSectionSize(400)
        self.gridTable.setIconSize(pyS.QtCore.QSize(400,400))
        #self.gridTable.setMinimumWidth(1200)
        self.mainGrid.addWidget(self.gridTable,pyS.QtCore.Qt.AlignTop)


        # self.scrollArea = pyS.QtWidgets.QScrollArea(self.homeWidget)
        # self.scrollArea.setWidgetResizable(True)
        # self.scrollAreaWidgetContents = pyS.QtWidgets.QWidget()
        # self.gridLayout = pyS.QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        # self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        # self.mainGrid.addWidget(self.scrollArea,pyS.QtCore.Qt.AlignTop)

    def buttonClick(self):
        userInput = self.entry.text()
        self.entry.setText("")
        killValue=self.orderServer(userInput)
        if(killValue):
            self.window.quit()

    def addMedia(self,serverResults):
        #delete widget and rebuild when new images called
        self.mainGrid.removeWidget(self.gridTable)
        self.gridTable.deleteLater()
        self.gridTable=None
        self.initScrollArea(math.ceil(len(serverResults)/3))

        self.homeWidget.show()
        self.mediaPlayers = []
        posInRow=0
        for i in range(0,len(serverResults)):
            if(posInRow == self.NUMROWS):
                posInRow = 0

            #as far as I know this line is superfulous idk, it doesn't change anything anymore
            # if(i%self.NUMROWS != 0):
            #     self.gridLayout.setRowMinimumHeight(math.trunc(i/self.NUMROWS),400)

            if serverResults[i][0].split(".")[-1]=="MP4":

                # self.mediaPlayers.append(playerWidget.VideoPlayer(serverResults[i][0]))
                # media=pyS.QtWidgets.QStyledItemDelegate(self.mediaPlayers[-1].getWidget())

                # #item.setSizeHint(pyS.QtCore.QSize(400,400))
                # self.gridTable.setItem(math.trunc(i/self.NUMROWS), posInRow, item)

                self.mediaPlayers.append(playerWidget.VideoPlayer(serverResults[i][0]))
                self.gridTable.setCellWidget(math.trunc(i/self.NUMROWS), posInRow, self.mediaPlayers[-1].getWidget())
                
            else:

                image = pyS.QtGui.QPixmap(serverResults[i][0].replace("\\","/"))
                image = image.scaled(400,400, pyS.QtCore.Qt.KeepAspectRatio)
                item = pyS.QtWidgets.QTableWidgetItem(pyS.QtGui.QIcon(image),"P")
                item.setSizeHint(pyS.QtCore.QSize(400,400))
                self.gridTable.setItem(math.trunc(i/self.NUMROWS), posInRow, item)

            posInRow+=1

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
                time.sleep(1)
            elif(command == "O" and not serverFlag):
                try:
                    fileLocation= guiInput[1]
                    fileName = guiInput[2]
                    if(os.path.isfile(fileLocation+fileName+"-dates.pkl") and os.path.isfile(fileLocation+fileName+"-faces.pk1")):
                        self.processQueue.put(["O", fileLocation, fileName])
                        time.sleep(1)
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


        serverFlag = self.serverInitializedEvent.is_set()
        if(serverFlag):
            self.serverStatus.setText("Server: ON")
        else:
            self.serverStatus.setText("Server: OFF")

        

        #False as we want killValue to be false
        return False




def main(processQueue, startEvent, returnQueue):
    serverGUI = GUI(processQueue, startEvent, returnQueue)
    serverGUI.exec()










# import os
# #from tkinter import *
# from tkinter import ttk
# import tkinter as tk
# import time
# from PIL import Image, ImageTk

# class MainGuiFrame(tk.Frame):

#     def __init__(self, parent,processQueue,serverIntializedEvent,resultQueue,*args, **kwargs):

#         self.processQueue=processQueue
#         self.serverIntializedEvent=serverIntializedEvent
#         self.resultQueue=resultQueue

#         tk.Frame.__init__(self, parent, *args, **kwargs)
#         #Object Frame
#         self.parent=parent
#         self.parent.geometry("800x1000")

#         #Object Label (commands)
#         self.label = tk.Label(self.parent, text="The following commands are: q(quit), s(save), ff(Find Face), fd(Find Date), ad(Add data)")
#         self.label.pack()

#         #Object server indicator
#         self.serverIndicator = tk.Label(self.parent, text="Server: OFF")
#         self.serverIndicator.pack()

#         #Object entry
#         self.entry = ttk.Entry(self.parent, width=35)
#         self.entry.focus_set()
#         self.entry.pack()

#         #object serverOutput dialogue
#         self.serverOutput = tk.Label(self.parent,text="")
#         self.serverOutput.pack()

#         #Object button
#         ttk.Button(master=self.parent, text = "Send Command", width=20, command=self.buttonPress).pack(pady=20)

#         #WIP
#         # #create verticle Scroll Bar for gallery frame
#         # self.verticleBar = tk.Scrollbar(self.parent, orient="vertical").pack(side="right",fill="y")

#         # #create gallary frame
#         # self.galFrame=tk.Frame(self.parent, width=750, height=750, yscrollcommand = self.verticleBar).pack(expand=True, fill="both")

#     def buttonPress(self):
#         userInput = self.entry.get()
#         self.entry.delete(0,"end")
#         if(userInput ==""):
#             return
#         killValue=self.orderServer(userInput)
#         if(killValue):
#             self.parent.destroy()

#     def orderServer(self,entry:str):
#         guiInput = entry.split(",")
#         command=guiInput[0].upper()
#         serverFlag = self.serverIntializedEvent.is_set()
#         if(command == ""):
#             pass
#         else:
#             if(command=="N" and not serverFlag):
#                 self.processQueue.put(["N", None, None])
#                 time.sleep(2)
#             elif(command == "O" and not serverFlag):
#                 try:
#                     fileLocation= guiInput[1]
#                     fileName = guiInput[2]
#                     if(os.path.isfile(fileLocation+fileName+"-dates.pkl") and os.path.isfile(fileLocation+fileName+"-faces.pk1")):
#                         self.processQueue.put(["O", fileLocation, fileName])
#                         time.sleep(2)
#                     self.serverOutput.configure(text="Successfully initalized")
#                 except:
#                     self.serverOutput.configure(text="Input failed, try again!")
#                     pass

#             #quit function
#             elif(command == "Q" and serverFlag):
#                 self.processQueue.put(["Q",None,None])
#                 return True

#             #save function
#             elif(command == "S" and serverFlag):
#                 filesaveLocation = guiInput[1]
#                 filesaveName = guiInput[2]
#                 if(os.path.exists(filesaveLocation)):
#                     self.processQueue.put(["S",filesaveLocation,filesaveName])
#                     self.serverOutput.configure(text="Save Successful")
#                 else:
#                     self.serverOutput.configure(text="USER ERROR: Invalid file path")

#             #Find face function
#             elif(command == "FF" and serverFlag):
#                 userRequest = guiInput[1]
#                 self.processQueue.put(["FF",userRequest,None])
#                 result = self.resultQueue.get()
#                 if(result == None):
#                     self.serverOutput.configure(text="Face not in database")
#                 else:
#                     self.serverOutput.configure(text=result)
#                     #self.guiGallery(result)

#             #Find date function
#             elif(command == "FD" and serverFlag):
#                 userRequest = guiInput[1]
#                 self.processQueue.put(["FD",userRequest,None])
#                 result = self.resultQueue.get()
#                 if(result == None):
#                     self.serverOutput.configure(text="Date Not in Database")
#                 else:
#                     self.serverOutput.configure(text=result)
#                     #self.guiGallery(result)

#             #add data
#             elif(command == "AD" and serverFlag):
#                 self.serverOutput.configure(text="User Function not yet implemented, suck it lol")

#             else:
#                 self.serverOutput.configure(text="Invalid command try again!")


#         serverFlag = self.serverIntializedEvent.is_set()
#         if(serverFlag):
#             self.serverIndicator.configure(text="Server: ON")
#         else:
#             self.serverIndicator.configure(text="Server: OFF")

        

#         #False as we want killValue to be false
#         return False

#     #WIP
#     # def guiGallery(self, result):
#     #     img_list=[ImageTk.PhotoImage(Image.open(x[0])) for x in result]
#     #     for i in range(int(len(result)/3)): # Number of rows
#     #         for j in range(3): # Number of columns
#     #             lbl = tk.Label(self.parent,image=img_list[3*i+j])
#     #             lbl.grid(row=i,column=j)

    

# def userInterface(processQueue, serverIntializedEvent, resultQueue):

#     win = tk.Tk()
#     MainGuiFrame(win,processQueue,serverIntializedEvent,resultQueue).pack(expand=True)
#     win.mainloop()















#     # win.geometry("750x1000")

#     # label = Label(win, text="The following commands are: q(quit), s(save), ff(Find Face), fd(Find Date), ad(Add data)")
#     # label.pack()

#     # serverIndicator = Label(win, text="Server: OFF")
#     # serverIndicator.pack()

#     # entry = ttk.Entry(win, width=35)
#     # entry.focus_set()
#     # entry.pack()

#     # serverOutput = Label(win,text="")
#     # serverOutput.pack()

#     # def buttonPress():
#     #     userInput = entry.get()
#     #     entry.delete(0,"end")
#     #     if(userInput ==""):
#     #         return
#     #     killValue=orderServer(userInput,serverIndicator,serverOutput,processQueue, serverIntializedEvent, resultQueue,win)
#     #     if(killValue):
#     #         win.destroy()

#     # ttk.Button(master=win, text = "Send Command", width=20, command=buttonPress).pack(pady=20)

    









#     # while(not serverIntializedEvent.is_set()):
#     #     userHistory = input("Would you like to use a database or create a new one? (n = new, o = old)").upper()
#     #     if(userHistory=="N"):
#     #         processQueue.put(["N", None, None])
#     #     elif(userHistory == "O"):
#     #         try:
#     #             fileLocation= input("What is the file location (don't forget \\ at end!)")
#     #             fileName = input("What is the file name?")
#     #             if(os.path.isfile(fileLocation+fileName+"-dates.pkl") and os.path.isfile(fileLocation+fileName+"-faces.pk1")):
#     #                 processQueue.put(["O", fileLocation, fileName])
#     #             print("Bad input, try again")
#     #         except:
#     #             print("Input failed, try again!")
#     #             pass
#     #     else:
#     #         print("Bad input, try again")

#     # #replace input w/ queue of arrays, each array has command (char) + filename/whatever else is needed!
#     # while(serverIntializedEvent):
#     #     userInput = input("Please enter your desired command: [h] help").upper()

#     #     #help function
#     #     if(userInput == "H"):
#     #         print("The following commands are: q(quit), s(save), ff(Find Face), fd(Find Date), ad(Add data)")

#     #     #quit function
#     #     elif(userInput == "Q"):
#     #         processQueue.put(["Q",None,None])

#     #     #save function
#     #     elif(userInput == "S"):
#     #         filesaveLocation = input("Enter location of save")+"\\"
#     #         filesaveName = input("Name of file")
#     #         if(os.path.exists(filesaveLocation)):
#     #             processQueue.put(["S",filesaveLocation,filesaveName])
#     #         else:
#     #             print("USER ERROR: Invalid file path")

#     #     #Find face function
#     #     elif(userInput == "FF"):
#     #         userRequest = input("Please enter the face of the desired person: ")
#     #         processQueue.put(["FF",userRequest,None])
#     #         result = resultQueue.get()
#     #         if(result == None):
#     #             print("Face not in database")
#     #         else:
#     #             print(result)

#     #     #Find date function
#     #     elif(userInput == "FD"):
#     #         userRequest = input("Please Enter the date (YEAR[XXXX]-MONTH[XX]-DAY[XX]): ")
#     #         processQueue.put(["FD",userRequest,None])

#     #     #add data
#     #     elif(userInput == "AD"):
#     #         print("User Function not yet implemented, suck it lol")

#     #     else:
#     #         print("Invalid command try again!")






# # if(userInput == "f"):
# #     userRequest = input("Please enter the face of the desired person: ")
# #     result = serverObject.getFace(userRequest)
# #     if(result == None):
# #         print("Person not found")
# #     else:
# #         print(result)
# # elif(userInput == "q"):
# #     print("Stopping Server")
# #     break
# # elif(userInput == "s"):
# #     while(True):
# #         try:
# #             filesaveLocation = input("Enter location of save")
# #             filesaveName = input("Name of file")
# #             serverObject.saveTable(filesaveName, filesaveLocation)
# #             break
# #         except:
# #             print("Save failed, please try again!")
# # else:
# #     print("Invalid command try again!")