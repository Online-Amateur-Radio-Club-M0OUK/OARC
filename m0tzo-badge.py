#!/usr/bin/python3
# -- coding: utf-8 --

# Fetches text from the api and displays it on the screen, made for OiFrog

# before running make sure you have python3, then install libraries:
# sudo pip3 install inky font_fredoka_one requests Pillow
import os
import argparse

import requests
from inky import InkyPHAT
from font_fredoka_one import FredokaOne
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

PATH = os.path.dirname(__file__)
API_URL = 'https://m.0tzo.me/index.php/api/statistics'

# Fetching the data from the API
try:
    resp = requests.get(API_URL, timeout=(15, 30))
    data = resp.json()
    TODAY_TEXT = "Today: " + data['Today']
    TOTAL_TEXT = "Total: " + data['total_qsos'] + " - " + datetime.now().strftime('%H:%M') 
    MONTH_TEXT = "Month: " + data['month_qsos']
    YEAR_TEXT  = "Year: " + data['year_qsos'] 

except Exception as e:
    print(e)
    TODAY_TEXT = 'Have QSO' + " - " + datetime.now().strftime('%H:%M') 
    MONTH_TEXT = 'or have a rest'
    YEAR_TEXT = 'de Cloudlog 73'
    TOTAL_TEXT = 'Check Back Shortly'



# Command line arguments to set display type and colour
try:
    parser = argparse.ArgumentParser()
    parser.add_argument('--colour', '-c', type=str, required=True, choices=["red", "black", "yellow"], help="ePaper display colour")
    args = parser.parse_args()
    colour = args.colour
except:
    print("Colour argument not given, so I ll use red")
    colour = 'red'

try:
    # Set up the display
    inky_display = InkyPHAT(colour)
    inky_display.set_border(inky_display.BLACK)

# Create the image
    image = Image.new('RGB', (212, 104),color=(255, 255, 255))
    font = ImageFont.truetype(FredokaOne, 20)
    draw = ImageDraw.Draw(image)

    draw.text((5, 0),  TODAY_TEXT, font=font, fill=(0, 0, 0))
    draw.text((45, 22), MONTH_TEXT, font=font, fill=(255, 0, 0))
    draw.text((85, 44), YEAR_TEXT, font=font, fill=(0, 0, 0))
    draw.text((5, 80), TOTAL_TEXT, font=font, fill=(255, 0, 0))
    palette = Image.new('P', (1, 1))
    palette.putpalette(
    [
        255, 255, 255,   # 0 = White
        0, 0, 0,         # 1 = Black
        255, 0, 0,       # 2 = Red (255, 255, 0 for yellow)
    ] + [0, 0, 0] * 253  # Zero fill the rest of the 256 colour palette
    )
    image = image.quantize(colors=3, palette=palette)
    image.save(os.path.join(PATH, "img.png"))
    img2 = Image.open(os.path.join(PATH, "img.png"))

    # Display the image
    inky_display.set_image(img2)
    inky_display.show()

    # Remove the image
    # os.remove(os.path.join(PATH, "img.png"))
    os.replace("/home/pi/Pimoroni/inkyphat/examples/img.png", "/home/pi/Pimoroni/inkyphat/examples/image/img.png")
except Exception as e:
    print(e)
