#! /usr/bin/env python3

import re
import os

import cv2
import numpy


METHOD = cv2.TM_CCOEFF_NORMED
ITEM_SIZE = (160, 160)


def load_input(input_path: str):
    path_list = os.listdir(input_path)
    return [cv2.imread(f'{input_path}/{path}') for path in path_list]


def load_digits():
    path_list = os.listdir('./digits')
    return [
        (get_digit_from_path(path), load_digit('./digits/' + path))
        for path in path_list
    ]


def load_items():
    path_list = os.listdir('./items')
    return [
        (get_item_id_from_path(path), load_item('./items/' + path))
        for path in path_list
    ]


def load_item(path: str) -> numpy.ndarray:
    rv = cv2.imread(path)
    rv = cv2.resize(rv, ITEM_SIZE, cv2.INTER_AREA)
    return rv


def get_item_id_from_path(path: str) -> str:
    rv = re.match(r'icon_equipment_(\d+)\.png', path)
    if not rv:
        return ''
    return rv.group(1)


def get_digit_from_path(path: str) -> int:
    rv = re.match(r'(-?\d)\.png', path)
    if not rv:
        return -1
    return int(rv.group(1))


def load_digit(path: str) -> numpy.ndarray:
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)


def get_item_count(source, item, digit_list, id):
    item = cv2.resize(item, (160, 160), cv2.INTER_AREA)
    rv = cv2.matchTemplate(source, item, METHOD)

    _min_value, max_value, _min_loc, max_loc = cv2.minMaxLoc(rv, None)

    if max_value < 0.8:
        return 0

    match_loc = max_loc

    min_y = match_loc[1] + 125
    max_y = match_loc[1] + item.shape[1] - 12
    min_x = match_loc[0] + 79
    max_x = match_loc[0] + item.shape[0] - 5
    display = source[min_y:max_y, min_x:max_x]

    display = cv2.cvtColor(display, cv2.COLOR_BGR2HSV)
    lower = numpy.array([0, 0, 60], dtype=numpy.uint8)
    upper = numpy.array([255, 255, 145], dtype=numpy.uint8)
    mask = cv2.inRange(display, lower, upper)
    mask = ~mask
    _y, x, _ = display.shape
    grid_list = [mask[:, x - 19 * (i + 1):x - 19 * i] for i in range(4)]

    total = 0
    for idx, grid in enumerate(grid_list):
        rv = get_digit(grid, digit_list, id, idx)
        if rv < 0:
            break
        total += rv * 10 ** idx

    # display = cv2.cvtColor(display, cv2.COLOR_HSV2BGR)
    # cv2.imwrite(f'/mnt/d/local/tmp/output/{total}_{id}.png', display)

    return total


def get_digit(grid, digit_list, id, idx):
    best_score = 0
    best_number = -1
    for number, digit in digit_list:
        rv = cv2.matchTemplate(grid, digit, METHOD)
        _min_value, max_value, _min_loc, _max_loc = cv2.minMaxLoc(rv, None)
        # print(id, idx, number, max_value, best_score)
        if max_value < best_score:
            continue
        best_score = max_value
        best_number = number
        if best_score > 0.75:
            break
    if best_score > 0.4:
        return best_number
    return -1
