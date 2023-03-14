import pygetwindow
import pyautogui
from PIL import Image

path = f"./screenshots"
titles = pygetwindow.getAllTitles()
x1, y1, width, height = pygetwindow.getWindowGeometry('sandeshgrg75- -bash - 80x24')
x2 = x1+width
y2 = y1+height
pyautogui.screenshot(path)
im = Image.open(path)
im = im.crop((x1, y1, x2, y2))
im.save(path)
im.show(path)