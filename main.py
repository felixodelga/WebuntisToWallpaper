from image_processing import drawTimetable
from timetable import getTimetable
from PIL import Image

import ctypes
import datetime
import os
import time
import random


def createWallpaper():

    # fetch random wallpaper
    img = Image.open(f'./img/img{random.randint(0, 9)}.jpg')

    # Get next 7 days and draw to wallpaper
    for i in range(7):
        timetable = getTimetable(
            datetime.datetime.today()+datetime.timedelta(days=i))
        drawTimetable(timetable, img, (0, 150*i, 400, 150+150*i))

    img.save('out.png')

    # set wallpaper
    ctypes.windll.user32.SystemParametersInfoW(
        20, 0, os.path.dirname(os.path.realpath(__file__)) + '\\out.png', 0)


# update every x minutes until deactivation
update_interval = 60 * 30  # 30 min

# try:
#     while True:

#         print("Setting Wallpaper...")
#         createWallpaper()
#         print("Wallpaper set successfully\n")
#         time.sleep(update_interval)

# except KeyboardInterrupt:
#     print("Exiting...")

createWallpaper()