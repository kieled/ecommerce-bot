from db import session
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import callbacks, localization, utils
from bot.markups import (
    addresses_markup,
    back_main_markup,
    cancel_markup,
    product_markup,
)
from bot.services import CustomerService, ProductService

ID, ADDRESS = range(2)


async def search_input(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.effective_message.edit_text(
        localization.find_product_message, reply_markup=back_main_markup
    )
    return ID


async def invalid_product_id(update: Update, _: ContextTypes.DEFAULT_TYPE):
    try:
        await update.effective_message.reply_text(
            localization.invalid_id_message, reply_markup=cancel_markup
        )
    except BadRequest:
        pass
    return ID


async def check_address(
    update: Update, context: ContextTypes.DEFAULT_TYPE, product_id: int | None = None
):
    context.user_data['product_id'] = (
        int(update.effective_message.text) if not product_id else product_id
    )

    async with session() as s:
        addresses = await CustomerService(s).get_addresses(update.effective_chat.id)
    if len(addresses):
        await update.effective_message.reply_text(
            localization.founded_addresses_message, reply_markup=addresses_markup(addresses)
        )
        return ConversationHandler.END
    else:
        return await buy_product(update, context, False)


async def buy_product(
    update: Update, context: ContextTypes.DEFAULT_TYPE, with_callback: bool = True
):
    if with_callback:
        await update.callback_query.answer()

        address_id = utils.get_id_from_callback(update.callback_query.data)
    else:
        address_id = None

    product_id = context.user_data.get('product_id')

    async with session() as s:
        if len(str(product_id)) > 5:
            product = None
        else:
            product = await ProductService(s, product_id).get_product_by_id()

    if not product:
        await update.effective_message.reply_text(
            localization.product_not_found_message, reply_markup=back_main_markup
        )
    else:
        message = await update.effective_message.reply_text(
            localization.product_founded_message(product),
            reply_markup=product_markup(product_id, address_id),
        )
        context.chat_data['last_keyboard_message'] = message.id
        context.user_data['price'] = product.price

        return ConversationHandler.END


find_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(search_input, callbacks.find_by_id)],
    states={
        ID: [
            MessageHandler(filters.Regex(r'^\d+$'), check_address),
            MessageHandler(filters.TEXT, invalid_product_id),
        ]
    },
    fallbacks=[utils.back_main_handler],
)

buy_handler = CallbackQueryHandler(buy_product, utils.callback_func(callbacks.address()))
