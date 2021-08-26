SHELL = '''
(() => {{
    const itemDict = {{
        {script}
    }};
    const itemList = JSON.parse(localStorage.itemList);
    for (const item of itemList) {{
        const eid = item.equipment_id;
        if (typeof itemDict[eid] !== 'undefined') {{
            item.count = itemDict[eid];
        }}
    }}
    localStorage.itemList = JSON.stringify(itemList);
}})();
'''

ITEM = '''
'{id}': {count},
'''


def generate_script(item_dict: dict[int, int]) -> str:
    call_list = []
    for id, count in item_dict.items():
        call_list.append(ITEM.format(id=id, count=count))
    return SHELL.format(script=''.join(call_list))
