def callback_func(objects: list[str]):
    def wrapper(data: object) -> bool:
        return str(data).split('_')[0] in objects

    return wrapper


def get_id_from_callback(callback_data: str) -> int | None:
    try:
        value = int(callback_data.split('_')[1])
        return value if value != 0 else None
    except ValueError:
        return None
