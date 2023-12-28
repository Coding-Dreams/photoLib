import exifread
from PIL import Image

from pillow_heif import register_heif_opener

register_heif_opener()

#image = open("D:\\Pictures\\iPhone\\iCloud Photos 3\\iCloud Photos\\IMG_5641.HEIC",'rb')
#exif = exifread.process_file(image, strict=True)
#print(str(exif['EXIF DateTimeOriginal']).replace(":","-").split(" ")[0])
#data = str(exif['EXIF DateTimeOriginal']).replace(":","-").split(" ")[0]
#print(exif)

image = Image.open("D:\\Pictures\\iPhone\\iCloud Photos 3\\iCloud Photos\\IMG_5641.HEIC")
exif = image.getexif()
print(exif.get(306).split(" ")[0].replace(":","-"))

exit()

import shutil
from PIL import Image
import PIL
from pillow_heif import register_heif_opener
from pillow_heif import register_avif_opener
import ffmpeg as ffm
import os
import ffmpy
import exifread


register_avif_opener()

register_heif_opener()


def importer(dirpath, file, convdir):

    fileType = file.split(".")[-1].upper()

    #Not a file we want to user
    if(fileType == "AAE"):
        return

    #FIX
    if(fileType == "GIF" or fileType == "WEBP"):
        pathToDir = f"{convdir}\\1900\\01\\01"
        shutil.copy2(dirpath+"\\"+file, convdir+f"{correctIndex(pathToDir)}")

    elif(fileType == "JPG"):
        #open the file
        img = Image.open(dirpath+"\\"+file)
        #get date
        #try:
        dateSeg = getDate(dirpath+"\\"+file).split("-")
        #except Exception:
        #    print("ERROR: getDate failed for: "+file)
        #create folders
        if(not createDir(convdir, dateSeg)):
            print(f"ERROR: {fileType} file creation...skipping this file: "+file)
            return
        #create file
        pathToDir = f"{convdir}\\{dateSeg[0]}\\{dateSeg[1]}\\{dateSeg[2]}\\"
        shutil.copy2(dirpath+"\\"+file, pathToDir+f"{correctIndex(pathToDir)}.JPG")

    #If MP4, just rename and move
    elif(fileType == "MP4"):
        input = ffm.probe(dirpath+"\\"+file)
        try:              
            date = input["format"]["tags"]["creation_time"].split("T")[0]
        except KeyError:
            date = "1900-01-01"
        except:
            print("ERROR DUNGOOFED")

        dateSeg = date.split("-")
        if(len(dateSeg) != 3):
            dateSeg = ["1900", "01", "01"]
            print("ERROR: .MP4 dateSeg not 3 characters")
            
        if(not createDir(convdir, dateSeg)):
            print("ERROR: .MP4 file creation...skipping this file: "+file)
            return
        
        pathToDir = f"{convdir}\\{dateSeg[0]}\\{dateSeg[1]}\\{dateSeg[2]}\\"

        shutil.copy2(dirpath+"\\"+file, pathToDir+f"{correctIndex(pathToDir)}.MP4")


    #If it is an MOV, we want to make it into an MP4, carry over the data, and put it into the correct folder (Date)
    elif(fileType == "MOV"):

        #input file
        input = ffm.probe(dirpath+"\\"+file) 

        #try to get date, if DNE make default (cannot be NULL)
        try:              
            date = input["format"]["tags"]["creation_time"].split("T")[0]
        except KeyError:
            date = "1900-01-01"
        except:
            print("ERROR DUNGOOFED")

        dateSeg = date.split("-")

        if(len(dateSeg) != 3):
            dateSeg = ["1900", "01", "01"]
            print("ERROR: .MOV dateSeg not 3 characters")

        #try to create folder hierarchy, if it exists ignore.
        if(not createDir(convdir, dateSeg)):
            print("ERROR: .MOV file creation...skipping this file: "+file)
            return

        pathToDir = f"{convdir}\\{dateSeg[0]}\\{dateSeg[1]}\\{dateSeg[2]}\\"

        ff = ffmpy.FFmpeg(global_options= ["-hwaccel cuda", "-hwaccel_output_format cuda","-hide_banner", "-loglevel error"]
                    ,inputs = {dirpath+"\\"+file:None},
                    outputs = {pathToDir+f"{correctIndex(pathToDir)}.MP4":"-c:v copy -c:a copy -movflags use_metadata_tags -map_metadata 0"})

        ff.run()

    #For HEICs -> copy metadata and change name to correct one
    elif(fileType == "HEIC" or fileType == "AVIF" or fileType == "PNG" or fileType == "JPEG"):
        #open the file
        img = Image.open(dirpath+"\\"+file)
        #get the EXIF info
        exifInfo = img.getexif()
        #get date
        #try:
        dateSeg = getDate(dirpath+"\\"+file).split("-")
        #except Exception:
        #    print("ERROR: getDate failed for: "+file)
        #    pass
        #create folders
        if(not createDir(convdir, dateSeg)):
            print(f"ERROR: {fileType} file creation...skipping this file: "+file)
            return
        #create file
        pathToDir = f"{convdir}\\{dateSeg[0]}\\{dateSeg[1]}\\{dateSeg[2]}\\"
        img.convert('RGB').save(pathToDir+str(correctIndex(pathToDir))+".JPG", exif = exifInfo)

    else:
        print("ERROR: Problem with: "+file+". Skipping")


def createDir(convdir, dateSeg):
    try:
        os.makedirs(f"{convdir}\\{dateSeg[0]}\\{dateSeg[1]}\\{dateSeg[2]}\\")
        return True
    except OSError:
        return True
    except:
        return False

def getDate(path):
    #buggy, find a better way
    try:
        image = open(path,'rb')
        exif = exifread.process_file(image, strict=True)
        print("You're not allowed here")
        return str(exif['EXIF DateTimeOriginal']).replace(":","-").split(" ")[0]
    except:
            image = Image.open(path)
            exif = image.getexif()
            return exif.get(3687)

    #except Exception:
    #    raise Exception

def correctIndex(dir_path):
    count = 0
    for path in os.scandir(dir_path):
        if path.is_file():
            count += 1
    return count



importer("D:\\Pictures\\iPhone\\iCloud Photos 3\\iCloud Photos","IMG_5641.HEIC", "D:\\Pictures\\")