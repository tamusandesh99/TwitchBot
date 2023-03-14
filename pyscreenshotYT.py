import pyscreenshot as ImageGrab
from datetime import datetime
import schedule
import time


def take_screenshot():
    print("ready to take screenshot")
    image_name = f"screensshot-{str(datetime.now())}"
    screenshot = ImageGrab.grab()
    filepath = f"./screenshots/{image_name}.png"
    screenshot.save(filepath)
    print("screenshot taken")
    return filepath


def main():
    schedule.every(5).seconds.do(take_screenshot())
    while True:
        schedule.run_pending()
        time.sleep(1)

