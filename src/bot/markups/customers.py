from db import CustomerAddress
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from bot import callbacks, localization


def addresses_markup(addresses: list[CustomerAddress]):
    keyboard_items = [
        [InlineKeyboardButton(address.address, callback_data=callbacks.address(address.id))]
        for address in addresses
    ]

    keyboard_items.append(
        [
            InlineKeyboardButton(localization.ADD_NEW, callback_data=callbacks.address(0)),
            InlineKeyboardButton(localization.TO_MAIN, callback_data=callbacks.back_main),
        ]
    )

    return InlineKeyboardMarkup(keyboard_items)
