import PIL.Image
import ffmpy
import PIL
import subprocess
import io
import base64

stdout=io.BytesIO()

script=ffmpy.FFmpeg(global_options=["-y","-loglevel error"],
                         inputs={"D:\\converted\\2022\\01\\01\\2.MP4":None},
                         outputs={"pipe:1":"-ss 00:00:01.000 -vframes 1 -c:v png -f image2pipe"})

stdout,garbase=script.run(stdout=subprocess.PIPE)

translated=io.BytesIO(stdout)

print(translated)

thumb=PIL.Image.open(translated)

thumb.show()

translated.close()


"""import ffmpy

script=ffmpy.FFmpeg(global_options=["-y"],
                         inputs={"D:\\converted\\2022\\01\\01\\2.MP4":None},
                         outputs={f"D:\\converted\\thumbnails\\thumbnail.png":"-ss 00:00:01.000 -vframes 1"})

script.run()
"""