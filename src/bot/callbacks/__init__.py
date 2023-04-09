find_by_id = 'find_product'
cancel = 'cancel'
back_main = 'back_main'
skip = 'skip'
paid = 'paid'


def callback_get(item_name: str, item_id: int | None = None) -> str | list[str]:
    return f'{item_name}_{item_id}' if item_id is not None else [item_name]


def buy(product_id: int | None = None):
    return callback_get('buy', product_id)


def color(color_id: int | None = None):
    return callback_get('color', color_id)


def size(size_id: int | None = None):
    return callback_get('size', size_id)


def address(address_id: int | None = None):
    return callback_get('address', address_id)
