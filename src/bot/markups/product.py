from telegram import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
from bot import schemas, callbacks, utils, localization


def product_markup(product_id: int, address: int | None = None):
    base_url = f'https://distortion.shop/order/{product_id}'
    if address:
        base_url += f'?address={address}'

    return ReplyKeyboardMarkup.from_row(
        button_row=[
            KeyboardButton(localization.BUY, web_app=WebAppInfo(url=base_url)),
            KeyboardButton(localization.TO_MAIN)
        ],
        resize_keyboard=True
    )


def product_color_markup(colors: list[schemas.ColorSchema], is_size=False):
    split = utils.split_list(colors, 4 if is_size else 2)

    keyboard_items = [[
        InlineKeyboardButton(color.name,
                             callback_data=callbacks.color(color.id)
                             if not is_size else callbacks.size(color.id)
                             ) for color in items] for items in split]

    keyboard_items.append([
        InlineKeyboardButton(localization.TO_MAIN, callback_data=callbacks.back_main)
    ])

    return InlineKeyboardMarkup(keyboard_items)


instagram_skip_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton(localization.SKIP, callback_data=callbacks.skip),
    InlineKeyboardButton(localization.TO_MAIN, callback_data=callbacks.back_main)
]])

product_payout_markup = InlineKeyboardMarkup([[
    InlineKeyboardButton(localization.CONFIRM, callback_data=callbacks.paid),
    InlineKeyboardButton(localization.TO_MAIN, callback_data=callbacks.back_main),
]])
