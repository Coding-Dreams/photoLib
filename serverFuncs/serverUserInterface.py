from flask import render_template
from flask import send_from_directory
from flask import send_file
from flask import Flask
from flask import request as rq
from flask import jsonify
import time
import os
import ffmpy
from waitress import serve
import threading
import io
import subprocess
#Linux Only
#import gunicornServer as gS


class GUI():

    def __init__(self, processQueue,serverInitializedEvent,resultQueue):
        #def app for flask
        #self.OPTIONS={"bind":"http://127.0.0.1:5000/",
        #              "workers":4}
        self.IMAGEFILELOC=os.path.abspath("D:\\converted")
        self.TEMPLATEFOLDER=os.path.abspath("C:\\Users\\nvbue\\Documents\\Niccolo von Bueren\\Projects\\photoLib\\serverFuncs\\templates\\")
        self.APP = Flask(__name__, static_folder=self.IMAGEFILELOC,template_folder=self.TEMPLATEFOLDER)
        #self.guniApp=gS.GunicornApp(self.APP, self.OPTIONS)

        #initialize Queues and events
        self.processQueue=processQueue
        self.serverInitializedEvent=serverInitializedEvent
        self.resultQueue = resultQueue

        self.serverStatus=self.serverInitializedEvent.is_set()
        self.commandStatus=""

        self.resultsToDisplay=[['placeHolder\\test.png']]


    def isServerOn(self):
        if self.serverStatus:
            return "ON"
        else:
            return "OFF"

    def orderServer(self,entry):
        guiInput = entry.split(",")
        command=guiInput[0].upper()
        if(command == ""):
            pass
        else:
            if(command=="N" and not self.serverStatus):
                self.processQueue.put(["N", None, None])
                time.sleep(1)
                self.serverStatus=self.serverInitializedEvent.is_set()
            elif(command == "O" and not self.serverStatus):
                try:
                    fileLocation= guiInput[1]
                    fileName = guiInput[2]
                    if(os.path.isfile(fileLocation+fileName+"-dates.pkl") and os.path.isfile(fileLocation+fileName+"-faces.pk1")):
                        self.processQueue.put(["O", fileLocation, fileName])
                        time.sleep(1)
                        self.serverStatus=self.serverInitializedEvent.is_set()
                        self.commandStatus="Successfully initialized"
                    else:
                        self.commandStatus="Initialization unsuccessful"
                except:
                    self.commandStatus="Input failed, try again!"
                    pass

            #quit function
            elif(command == "Q"):
                self.processQueue.put(["Q",None,None])
                print("GUI: GUI SHUTTING DOWN")
                exit()

            #save function
            elif(command == "S" and self.serverStatus):
                filesaveLocation = guiInput[1]
                filesaveName = guiInput[2]
                if(os.path.exists(filesaveLocation)):
                    self.processQueue.put(["S",filesaveLocation,filesaveName])
                    self.commandStatus="Save Successful"
                else:
                    self.commandStatus="USER ERROR: Invalid file path"

            #Find face function
            elif(command == "FF" and self.serverStatus):
                userRequest = guiInput[1]
                self.processQueue.put(["FF",userRequest,None])
                result = self.resultQueue.get()
                if(result == None):
                    self.commandStatus="Face not in database"
                else:
                    self.commandStatus="Face Found"
                    self.resultsToDisplay=result

            #Find date function
            elif(command == "FD" and self.serverStatus):
                userRequest = guiInput[1]
                self.processQueue.put(["FD",userRequest,None])
                result = self.resultQueue.get()
                if(result == None):
                    self.commandStatus="Date Not in Database"
                else:
                    self.commandStatus="Date Found"
                    self.resultsToDisplay=result

            #add data
            elif(command == "AD" and self.serverStatus):
                self.commandStatus="User Function not yet implemented, suck it lol"

            else:
                self.commandStatus="Invalid command try again!"

        #False as we want killValue to be false
        return

    def exec(self):
        """
        @self.app.route('/')
        def home():
            return render_template('gallery.html')
        """
        @self.APP.route('/',methods=['GET','POST'])
        def home(): #reqs old name
            if rq.method=='POST':
                command=rq.form['shit']
                self.orderServer(command)
                return render_template('gallery.html', serverStatus=self.isServerOn(),
                    serverResponse=self.commandStatus)
            #else:
            return render_template('gallery.html')
        
        @self.APP.route('/getJQuery', methods=['GET'])
        def getJQuery():
            return send_from_directory(self.TEMPLATEFOLDER,"jquery-3.7.1.min.js")
        
        @self.APP.route('/getImageArray', methods=['GET'])
        def getArr():
            return jsonify({"imageLocs":self.resultsToDisplay}) #jsonify(self.resultsToDisplay)
 
        @self.APP.route('/getImage/<path:filename>',methods=['GET'])
        def imageShake(filename):
            #print(filename)
            #print(self.IMAGEFILELOC)
            return send_from_directory(self.IMAGEFILELOC,filename.replace('D:/converted/',''))
        
        @self.APP.route('/getThumbnail/<path:filename>',methods=['GET'])
        def getThumbnail(filename):
            stdout=io.BytesIO()
            script=ffmpy.FFmpeg(global_options=["-y","-loglevel error"],
                                    inputs={filename:None},
                                    outputs={"pipe:1":"-ss 00:00:01.000 -vframes 1 -c:v png -f image2pipe"})
            stdout,garbage=script.run(stdout=subprocess.PIPE)
            del garbage
            translated=io.BytesIO(stdout)
            return send_file(translated, mimetype='image/png')

            """
            uniqID=threading.get_ident()
            ffscript=ffmpy.FFmpeg(global_options=["-y","-loglevel error"],
                         inputs={filename:None},
                         outputs={f"{self.IMAGEFILELOC}\\thumbnails\\thumbnail-{uniqID}.png":"-ss 00:00:01.000 -vframes 1"})
            ffscript.run()
            return send_file(f"{self.IMAGEFILELOC}\\thumbnails\\thumbnail-{uniqID}.png")
            """
        
        serve(self.APP, threads=12, port=5000)
        #self.guniApp.run()
        #self.APP.run(threaded=True)

def main(processQueue, startEvent, returnQueue):
    serverGUI = GUI(processQueue, startEvent, returnQueue)
    serverGUI.exec()

#main(None, None, None)