import argparse
import concurrent.futures
import os
import os.path
import sys

from .adb import grab_input
from .ocr import BitMap, DigitList, load_digits, load_items, load_input, get_item_count
from .output import generate_script


def main(args: list[str] = None) -> int:
    if args is None:
        args = sys.argv
    kwargs = parse_args(args[1:])
    if kwargs.auto_screen_shot:
        grab_input(kwargs.input_folder, kwargs.adb_path)

    input_list = load_input(kwargs.input_folder)
    digit_list = load_digits()
    item_list = load_items()

    item_dict: dict[str, int] = {}
    with concurrent.futures.ProcessPoolExecutor() as pool:
        task_list = [
            pool.submit(find_item_count, input_list, id, item, digit_list)
            for id, item in item_list
        ]
        for task in concurrent.futures.as_completed(task_list):
            try:
                id, count = task.result()
                item_dict[id] = count
                print(id, count)
            except Exception as e:
                print(id, e)
    script = generate_script(item_dict)

    with open(kwargs.output_file, 'w') as fout:
        fout.write(script)

    return 0


def parse_args(args: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser('pcrd')

    parser.add_argument('input_folder', type=str, help='folder contains item screen shots (e.g. ./input/)')
    parser.add_argument('output_file', type=str, help='file name of JS output (e.g. ./output.js)')
    add_bool_argument(parser, 'auto_screen_shot', 'A',
        default=True,
        yes_help='enable auto screen shot (need adb) (default: enable)',
        no_help='disable auto screen shot',
    )
    parser.add_argument('--adb-path', type=str, action='store', default='adb')

    kwargs = parser.parse_args(args)
    check_args(kwargs)
    return kwargs


def check_args(kwargs: argparse.Namespace):
    if not os.path.isdir(kwargs.input_folder):
        raise argparse.ArgumentError(None, f'input folder {kwargs.input_folder} not found')
    if kwargs.auto_screen_shot:
        if os.listdir(kwargs.input_folder):
            raise argparse.ArgumentError(None, f'input folder {kwargs.input_folder} is not empty')


def add_bool_argument(
    parser: argparse.ArgumentParser,
    name: str,
    short_name: str = None,
    *,
    default: bool = True,
    yes_help: str = None,
    no_help: str = None,
) -> None:
    flag = name.replace('_', '-')
    pos_flags = ['--' + flag]
    if short_name:
        pos_flags.append('-' + short_name)
    neg_flag = '--no-' + flag
    pos_default = default
    neg_default = not default
    parser.add_argument(*pos_flags, dest=name, action='store_true', default=pos_default, help=yes_help)
    parser.add_argument(neg_flag, dest=name, action='store_false', default=neg_default, help=no_help)


def find_item_count(input_list: list[BitMap], id: str, item: BitMap, digit_list: DigitList) -> tuple[str, int]:
    rv: int = 0
    for input_ in input_list:
        count = get_item_count(input_, item, digit_list)
        if count > rv:
            rv = count
            break
    return id, rv
