import argparse
import sys

from .ocr import load_digits, load_items, load_input, get_item_count
from .output import generate_script


def main(args: list[str] = None) -> int:
    if args is None:
        args = sys.argv
    kwargs = parse_args(args[1:])

    input_list = load_input(kwargs.input_folder)
    digit_list = load_digits()
    item_list = load_items()

    item_dict = {}
    for id, item in item_list:
        for input_ in input_list:
            count = get_item_count(input_, item, digit_list, id)
            if count > item_dict.get(id, 0):
                item_dict[id] = count
                print(id, count)
                break
    script = generate_script(item_dict)

    with open(kwargs.output_file, 'w') as fout:
        fout.write(script)

    return 0


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser('pcrd')

    parser.add_argument('input_folder', type=str, default='./input')
    parser.add_argument('output_file', type=str, default='./output.js')

    kwargs = parser.parse_args(args)
    return kwargs
