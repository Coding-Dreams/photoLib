import os
import PIL.Image
import PIL
import json

def main():

    rootdir = "D:\\Pictures\\iPhone Photos 2"
    picoutdir = "D:\\webp4db"
    jsonoutdir = "D:\\json4db\\serverDB.json"

    def convertAndSaveFunc(file, id):

        jsonDict = {}

        jsonDict["id"] = id

        #print(file)

        #if(file.split(".")[-1] == "MP4" or file.split(".")[-1] == "HEIC" or file.split(".")[-1] == "MOV" or file.split(".")[-1] =="AAE"\
        #   or file.split(".")[-1] == "AVIF"):
        #    return
        
        img = PIL.Image.open(file)
        
        #Get file date
        try:
            #print({PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS}['DateTimeOriginal'])
            jsonDict["Date"] = str({PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS}['DateTimeOriginal'])

        except:
            jsonDict["Date"] = "2001:01:01 00:00:00"

        #get GPS MetaData
        try:
            exif = {PIL.ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in PIL.ExifTags.TAGS}
            gpsInfo={}
            for key in exif["GPSInfo"].keys():
                decode = PIL.ExifTags.GPSTAGS.get(key,key)
                gpsInfo[decode] = exif['GPSInfo'][key]

            #print((gpsInfo["GPSLatitude"]))

            lat = list(gpsInfo["GPSLatitude"])#[n/d for n, d in gpsInfo["GPSLatitude"]]
            lon = list(gpsInfo["GPSLongitude"])#[n/d for n, d in gpsInfo["GPSLongitude"]]

            if(gpsInfo["GPSLatitudeRef"] == "N"):
                finLat = round(lat[0]+lat[1]/60.0+lat[2]/3600.0,9)
            else:
                finLat = round(-1*(lat[0]+lat[1]/60.0+lat[2]/3600.0),9)

            if(gpsInfo["GPSLongitudeRef"] == "E"):
                finLon = round(lon[0]+lon[1]/60.0+lon[2]/3600.0,9)
            else:
                finLon = round(-1*(lon[0]+lon[1]/60.0+lon[2]/3600.0),9)

            jsonDict["GPSLatitudeRef"] = gpsInfo["GPSLatitudeRef"]
            jsonDict["GPSLatitude"] = finLat
            jsonDict["GPSLongitudeRef"] = gpsInfo["GPSLongitudeRef"]
            jsonDict["GPSLongitude"] = finLon
            jsonDict["GPSAltitude"] = round(gpsInfo["GPSAltitude"],9)

        except:
            jsonDict["GPSLatitudeRef"] ='N'
            jsonDict["GPSLatitude"] = 0.0
            jsonDict["GPSLongitudeRef"] = 'E'
            jsonDict["GPSLongitude"] = 0.0
            jsonDict["GPSAltitude"] = 0.0

        #print(jsonDict)

        jsonDict["filepath"] = file.replace("\\","//")

        #jdict = {"name": file.split(".")[0] + img., }


        #jsonfile = file()

        return jsonDict

    flag = 0

    arr=[]

    for dirpath, dirnames, files in os.walk(rootdir):
        for file in files:
            #aae is useless
            #HEIC can be converted
            if(file.split(".")[-1] == "MP4" or file.split(".")[-1] == "HEIC" or file.split(".")[-1] == "MOV" or file.split(".")[-1] =="AAE"\
        or file.split(".")[-1] == "AVIF"):
                pass
            else:
                arr.append(convertAndSaveFunc(dirpath+"\\"+file, flag))
                flag+=1

    #print(arr)
        

    return arr
    
    #outfile = open(jsonoutdir, 'x')
    #outfile.write(json.dumps(arr))
    #outfile.close()

    #with open(jsonoutdir, 'x') as outfile:
    #    json.dump(arr, outfile)
    #outfile.close()



    # import json
    # import base64

    # data ={}
    # with open("D:\\Pictures\\iPhone Photos 2\\2023-09-26\\2023-09-26 005.JPG",mode='rb') as file:
    #     img = file.read()

    # data['img'] = base64.encodebytes(img).decode('utf-8')

    # file = open("D:\\Pictures\\iPhone Photos 2\\2023-09-26\\2023-09-26 005.json", 'x')
    # file.write(json.dumps(data))
    
#main()