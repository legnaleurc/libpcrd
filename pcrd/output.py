SHELL = '''
(() => {{
    function updateCount (id, count) {{
        const input = document.querySelector(`.itemBox > img[src$="${{id}}.png"] + input`);
        input.value = count;
        input.dispatchEvent(new Event('input'));
    }}
    {script}
}})();
'''

ITEM = '''
updateCount({id}, {count});
'''


def generate_script(item_dict):
    call_list = []
    for id, count in item_dict.items():
        call_list.append(ITEM.format(id=id, count=count))
    return SHELL.format(script=''.join(call_list))
