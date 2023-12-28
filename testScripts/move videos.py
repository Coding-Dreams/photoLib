import os
import shutil

rootdir = "D:\\Pictures"
convdir = "D:\\converted"

flag = 0

for dirpath, dirnames, files in os.walk(rootdir):
        for file in files:
            #aae is useless
            #HEIC can be converted
            try:
                if(file.split(".")[-1].upper() == "MP4" or  file.split(".")[-1].upper() == "MOV"):
                    shutil.copy2(dirpath+"\\"+file, convdir+"\\"+file)
                    flag+=1
                elif(file.split(".")[-1].upper() == "HEIC" or file.split(".")[-1].upper() =="AAE" or file.split(".")[-1].upper() == "AVIF" or file.split(".")[-1].upper() == "JPG" or file.split(".")[-1].upper() == "PNG" or file.split(".")[-1].upper() == "JPEG"):
                    pass
                else:
                    print("ERROR: " + file)
            except:
                 print(file+" did not work")
                 pass


print(flag)