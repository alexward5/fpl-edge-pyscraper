def set_data_type(value: str, data_type: str):
    if data_type == "str":
        return str(value)
    elif data_type == "int":
        return int(value)
    elif data_type == "float":
        return float(value)
    else:
        raise ValueError("Unsupported data type found in config")
