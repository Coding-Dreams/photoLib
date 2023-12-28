import os
#from PIL import Image
import PIL
from pillow_heif import register_heif_opener

register_heif_opener()

path = "D:\\Pictures\\iPhone 3\\2023-12-02\\2023-12-02 001.JPG"

img = PIL.Image.open(path)

fuck = img.getexif()

exif = {PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS}

#this is the date created
try:
    date = exif["DateTimeOriginal"].split(" ")[0].replace(":","-")
except KeyError:
    date = "1900-01-01"
except:
    print("ERROR:")


# for dirpath, dirnames, files in os.walk(rootdir):
#         for file in files:
#             #aae is useless
#             #HEIC can be converted
#             try:
#                 if()
#                 if(file.split(".")[-1].upper() == "MP4" or  file.split(".")[-1].upper() == "MOV" or file.split(".")[-1].upper() =="AAE" or file.split(".")[-1].upper() == "AVIF"):
#                     pass
#                 elif(file.split(".")[-1] == "HEIC"):
#                     img = Image.open(dirpath+"\\"+file)
#                     fuck = img.getexif()
#                     newfile = file.split(".")[0]+".jpg"
#                     img.convert('RGB').save(convdir+"\\"+newfile, exif = fuck)
#                     flag+=1
#                 else:
#                     img = Image.open(dirpath+"\\"+file)
#                     fuck = img.getexif()
#                     img.save(convdir+"\\"+file, exif = fuck)
#                     flag+=1
#             except:
#                  print(file+" did not work")
#                  pass


