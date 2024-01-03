# import exifread
# from PIL import Image


# def getDate(path):
#     #buggy, find a better way
#     #try:
#     image = open(path,'rb')
#     exif = exifread.process_file(image, strict=False)
#     image.close()
#     return str(exif['EXIF DateTimeOriginal']).replace(":","-").split(" ")[0]
#     # except:
#     #     try:
#     #         image = Image.open(path)
#     #         exif = image.getexif()
#     #         if exif.get(36867) == None and exif.get(36868) == None and exif.get(306) == None:
#     #             return "1900-01-01"
#     #         else:
#     #             if exif.get(36867) != None:
#     #                 print("Yo")
#     #                 return exif.get(36867)
#     #             elif exif.get(36868) != None:
#     #                 return exif.get(36868)
#     #             else:
#     #                 return "1900-01-01"
#     #     except KeyError:
#     #         return "1900-01-01"
#     #     except AttributeError:
#     #         return "1900-01-01"
        

# print(getDate("D:\\Pictures\\iPhone 3\\2023-11-27\\2023-11-27 010.JPG"))



import ffmpeg as ffm

input = ffm.probe("D:\\converted\\1900\\01\\01\\295.MP4")
try:              
    print(input)
    date = input["format"]["tags"]["com.apple.quicktime.creationdate"].split("T")[0]

except:
    try:
        date = input["format"]["tags"]["creation_time"].split("T")[0]

        #Im not going down the pitful of timezones, I know there is date module which probably would've fixed everything but it is not worth the time 
        # #if the hour leads to a previous day then:
        # if(creationTimeHourUTC - 8 <= 0):
        #     creationDateDay = int(creationDate[0].split("-")[-1])

        #     #if the day-1 leads to a previous month then:
        #     if(creationDateDay-1 <= 0):
        #         creationDateMonth = int(creationDate[0].split("-")[1]) - 1
        #         creationDateYear = int(creationDate[0].split("-"[0]))

        #         #if the month leads to a previous year then:
        #         if(creationDateMonth <= 0):
        #             date=str(creationDateYear-1)+"-12-31"
        #         else:
        #             date=str(creationDateYear)+"-"+str(creationDateMonth)+"-"+str( int(i/2), 0 if i%2==0 else 31 )
    except KeyError:
        date = "1900-01-01"
    except:
        print("ERROR DUNGOOFED")

print(date)
date=date.split("-")
print(len(date))


# # input = ffm.probe("D:\\converted\\2023\\01\\03\\"+"0.MP4")
# # try:              
# #     print(input)
# #     date = input["format"]["tags"]["com.apple.quicktime.creationdate"].split("T")[0]
# # except KeyError:
# #     date = "1900-01-01"
# # except:
# #     print("ERROR DUNGOOFED")

# # print(date)

# #difference: com.apple.quiktime.creationdate is local
# #creation_time is UTC
# #I'll be honest, I cannot care about the accuracy of this too much lol - timezones are difficult :( and if 1 in every 1000 pictures are wrong it's kinda whatever.