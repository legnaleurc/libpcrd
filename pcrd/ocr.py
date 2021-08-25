#! /usr/bin/env python3

import re
import os

import cv2
import numpy
import pytesseract


METHOD = cv2.TM_CCOEFF_NORMED


def load_input():
    path_list = os.listdir('./input')
    return [cv2.imread('./input/' + path) for path in path_list]


def load_items():
    path_list = os.listdir('./items')
    return [
        (re.match(r'icon_equipment_(\d+)\.png', path).group(1), cv2.imread('./items/' + path))
        for path in path_list
    ]


def get_item_count(source, item):
    item = cv2.resize(item, (160, 160), cv2.INTER_AREA)
    rv = cv2.matchTemplate(source, item, METHOD)

    _min_value, max_value, _min_loc, max_loc = cv2.minMaxLoc(rv, None)

    if max_value < 0.8:
        return 0

    match_loc = max_loc

    min_y = match_loc[1] + 120
    max_y = match_loc[1] + item.shape[1] - 5
    min_x = match_loc[0] + 80
    max_x = match_loc[0] + item.shape[0] - 5
    display = source[min_y:max_y, min_x:max_x]

    display = cv2.cvtColor(display, cv2.COLOR_BGR2HSV)
    lower = numpy.array([0, 0, 70], dtype=numpy.uint8)
    upper = numpy.array([255, 255, 125], dtype=numpy.uint8)
    mask = cv2.inRange(display, lower, upper)
    mask = ~mask

    config = '--oem 3 --psm 6 outputbase digits'
    rv = pytesseract.image_to_string(mask, lang='eng', config=config)
    rv = re.sub('\D', '', rv)
    if not rv:
        return 0
    rv = int(rv, 10)
    return rv
