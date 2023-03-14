import json

from twitchio.ext import commands
import config
import mss
import mss.tools
import time
from PIL import Image
from pytesseract import pytesseract


def main():
    """ Start of the screen capture """
    total_run = get_count()  # Getting the total run stored in json file
    myconfig = r"--psm 3 --oem 3"  # initializing the configuration for tesseract
    with mss.mss() as sct:
        while True:
            monitor_number = 2  # screenshot pointing to 2nd monitor
            mon = sct.monitors[monitor_number]

            # The screen part to capture. Captures the center of screen
            monitor_died = {
                "top": mon["top"] + 410,  # 410px from the top
                "left": mon["left"] + 550,  # 550px from the left
                "width": 450,
                "height": 160,
                "mon": monitor_number,
            }
            #  Screen to capture. Captures the center bottom of screen
            monitor_blade = {
                "top": mon["top"] + 710,  # 100px from the top
                "left": mon["left"] + 550,  # 100px from the left
                "width": 450,
                "height": 110,
                "mon": monitor_number,
            }

            #  describing path and file name for screenshot
            output_died = "./screenshots/died.png".format(**monitor_died)
            output_blade = "./screenshots/blade.png".format(**monitor_died)

            # Grabs the screenshot of two positions in screen
            sct_img_died = sct.grab(monitor_died)
            sct_img_blade = sct.grab(monitor_blade)

            # Save to the picture file (png)
            mss.tools.to_png(sct_img_died.rgb, sct_img_died.size, output=output_died)
            mss.tools.to_png(sct_img_blade.rgb, sct_img_blade.size, output=output_blade)

            #  sending the screenshot to tesseract to convert it to text
            text_died = pytesseract.image_to_string('./screenshots/died.png', config=myconfig)
            text_blade = pytesseract.image_to_string('./screenshots/blade.png', config=myconfig)

            # Original to match with screenshot texts
            dialogues = ['Malenia', 'Blade', 'Miquella',
                         'Flesh', 'Let', 'Your', 'be', 'consumed',
                         'By', 'scarlet', 'rot']
            deathMark = ['YOU', 'DIED', 'OUD', 'OU', 'IED', 'YO']

            # print(text_died)
            # print(text_blade)
            #  Compares if the texts in screenshot matches with default condition text
            if any([x in text_blade for x in dialogues]):
                print("Blade")
                total_run += 1
                update_count(total_run)  # update the value in json if conditions met
                time.sleep(7)
            if any([x in text_died for x in deathMark]):
                print('Died')
                total_run += 1
                update_count(total_run)  # update the value in json if conditions met
                time.sleep(5)
            print(total_run)


def get_count():
    """ Reads the count from the JSON file and returns it """
    with open(config.JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['total_run']


def update_count(count):
    """ Updates the JSON file with count given """
    data = None

    with open(config.JSON_FILE) as json_file:
        data = json.load(json_file)

    if data is not None:
        data['total_run'] = count

    with open(config.JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()

