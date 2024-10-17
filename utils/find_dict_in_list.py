def find_dict_in_list(list_of_dicts: list[dict], key: str, value: str):
    for dict_item in list_of_dicts:
        if dict_item.get(key) == value:
            return dict_item

    return None
