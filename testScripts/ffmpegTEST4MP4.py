import ffmpeg as ffm
import ffmpy

input = ffm.probe("D:\\Pictures\\iPhone\\Photos\\recorded-13645009663175.mp4")
#input = ffmpeg.probe("D:\\Pictures\\iPhone 3\\2023-11-27\\2023-11-27 006.MOV")

try:
    location = input["format"]["tags"]["com.apple.quicktime.location.ISO6709"]
    arr_location =[]
    for character in location:
        if(character == "/"):
            break
        elif(character != "+" and character != "-"):
            arr_location[-1]+=character
        else:
            arr_location.append(character)
    location = {"Latitude":arr_location[0], "Longitude":arr_location[1], "Altitude":arr_location[2]}
except KeyError:
    print("No Location Default")
except:
    print("ERROR DUNGOOFED")

try:              
    date = input["format"]["tags"]["creation_time"].split("T")[0]
except KeyError:
    date = "1900-01-01"
except:
    print("ERROR DUNGOOFED")


print(date)

# ff = ffmpy.FFmpeg(global_options= ["-hwaccel cuda", "-hwaccel_output_format cuda"]
#                   ,inputs = {"D:\\Pictures\\iPhone 3\\2023-12-02\\2023-12-02 002.MOV":None},
#                   outputs = {f"D:\\Pictures\\"+date+".MP4":"-c:v copy -c:a copy -movflags use_metadata_tags -map_metadata 0"})

# ff.run()

exit
