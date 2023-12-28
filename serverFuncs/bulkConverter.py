import pictureImport
import os
import time

def Importer(serverQueue, serverIntializedEvent):

    while(not serverIntializedEvent.is_set()):
         time.sleep(1)

    rootdir = "D:\\Pictures"
    convdir = "D:\\converted"

    for dirpath, dirnames, files in os.walk(rootdir):
            for file in files:
                pathToImg = pictureImport.importer(dirpath, file, convdir)
                if(pathToImg==None):
                    pass
                else:
                    serverQueue.put(["AD",[pathToImg,None],None])
