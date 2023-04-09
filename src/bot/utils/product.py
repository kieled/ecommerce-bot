def split_list(items: list, step: int = 3) -> list:
    return [items[x : x + step] for x in range(0, len(items), step)]
