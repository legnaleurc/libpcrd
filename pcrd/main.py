import argparse
import concurrent.futures
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

    item_dict: dict[str, int] = {}
    with concurrent.futures.ProcessPoolExecutor() as pool:
        task_list = [
            pool.submit(find_item_count, input_list, digit_list, id, item)
            for id, item in item_list
        ]
        for task in concurrent.futures.as_completed(task_list):
            try:
                id, count = task.result()
                item_dict[id] = count
            except Exception as e:
                print(id, e)
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


def find_item_count(input_list, digit_list, id, item) -> tuple[str, int]:
    rv: int = 0
    for input_ in input_list:
        count = get_item_count(input_, item, digit_list, id)
        if count > rv:
            rv = count
            break
    return id, rv
