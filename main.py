import json
import configuration
import mss
import mss.tools
import time
from pytesseract import pytesseract


def main():
    """ Start of the screen capture """
    myconfig = r"--psm 3 --oem 3"  # initializing the configuration for tesseract
    with mss.mss() as sct:
        while True:
            total_run = get_count()  # Getting the total run stored in json file
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
            text_died = pytesseract.image_to_string('./screenshots/died.png', configuration=myconfig)
            text_blade = pytesseract.image_to_string('./screenshots/blade.png', configuration=myconfig)

            # Default texts to match with screenshot texts
            dialogues = ['Malenia', 'Blade', 'Miquella',
                         'Flesh', 'Your', 'consumed',
                         'scarlet', 'rot', 'Let']
            deathMark = ['YOU', 'DIED']

            #  Compares if the texts in screenshot matches with default condition text
            if any([word in text_blade for word in dialogues]):
                print("Blade")
                print(text_blade)
                time.sleep(3)
                total_run += 1
                update_count(total_run)  # update the value in json if conditions met
                time.sleep(9)

            if any([word in text_died for word in deathMark]):
                print('Died')
                print(text_died)
                time.sleep(3)
                total_run += 1
                update_count(total_run)  # update the value in json if conditions met
                time.sleep(8)
            print(total_run)


def get_count():
    """ Reads the count from the JSON file and returns it """
    with open(configuration.JSON_FILE) as json_file:
        data = json.load(json_file)
        return data['total_run']


def update_count(count):
    """ Updates the JSON file with count given """
    data = None

    with open(configuration.JSON_FILE) as json_file:
        data = json.load(json_file)

    if data is not None:
        data['total_run'] = count
        data['send_run'] = True

    with open(configuration.JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, sort_keys=True, indent=4)


if __name__ == '__main__':
    main()

