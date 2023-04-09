from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from bot import callbacks, localization


welcome_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton(localization.ID_SEARCH, callback_data=callbacks.find_by_id)
    ],
    [
        InlineKeyboardButton(localization.INST, url='https://instagram.com/disstortion.store/'),
        InlineKeyboardButton(localization.WEBSITE, url='https://distortion.shop/')
    ],
    [
        InlineKeyboardButton(localization.SUPPORT, url='https://t.me/distortionsup')
    ]
])

cancel_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton(localization.CANCEL, callback_data=callbacks.back_main)]
])

skip_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton(localization.SKIP, callback_data=callbacks.skip)]
])

back_main_markup = InlineKeyboardMarkup([
    [InlineKeyboardButton(localization.TO_MAIN, callback_data=callbacks.back_main)]
])
