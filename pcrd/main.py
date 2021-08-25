from .ocr import load_items, load_input, get_item_count
from .output import generate_script


def main():
    input_list = load_input()
    item_list = load_items()

    item_dict = {}
    for id, item in item_list:
        for input_ in input_list:
            count = get_item_count(input_, item)
            if count > item_dict.get(id, 0):
                item_dict[id] = count
                print(id, count)
                break
    script = generate_script(item_dict)

    with open('./output.js', 'w') as fout:
        fout.write(script)

    return 0
