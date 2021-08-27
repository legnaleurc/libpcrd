#! /usr/bin/env python3

import subprocess
import time

import cv2
import numpy


def grab_screenshot() -> numpy.ndarray:
    with subprocess.Popen('adb shell screencap -p', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True) as pipe:
        image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
    np_arr = numpy.frombuffer(image_bytes, numpy.uint8)
    return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


def swipe(x1: int, y1: int, x2: int, y2: int, duration: int) -> None:
    subprocess.call(f'adb shell input swipe {x1} {y1} {x2} {y2} {duration}')


def get_coordinates(h: int, w: int) -> tuple:
    return w // 2, 3 * h // 4, w // 2, h // 3.5


def get_bottom_point(h: int, w: int) -> tuple:
    return 749 * h // 900, 977 * w // 1600


def get_color_diff(a: tuple, b: tuple) -> int:
    ret = 0
    power = [2, 4, 3]
    for i in range(3):
        ret += power[i] * (a[i] - b[i]) ** 2
    return ret


def grab_input(input_folder: str):
    coordinates = None
    scroll_bar_bottom_point = None
    idx = 0
    while True:
        img = grab_screenshot()
        if not coordinates:
            h, w, _ = img.shape
            coordinates = get_coordinates(h, w)
            scroll_bar_bottom_point = get_bottom_point(h, w)
        cv2.imwrite(f'{input_folder}/{idx}.png', img)
        if get_color_diff(img[scroll_bar_bottom_point], (191, 123, 88)) < 200:
            break
        swipe(*coordinates, 500)
        time.sleep(0.5)
        idx += 1
