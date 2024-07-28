import subprocess
import sys

def install(package):
    subprocess.call(["python3","-m","pip","install",package,'--progress-bar=on'])
    return

listOfPackages=['os','time','shutil','pillow','pillow_heif','ffmpy','ffmpeg','exifread','pickle',
                'multiprocess','waitress','flask']

for package in listOfPackages:
    install(package)
