from db import session
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from bot import callbacks, localization, markups, schemas, services, utils

from .find_handler import check_address

INST = range(1)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.chat_data.get('last_keyboard_message'):
        await context.bot.delete_message(
            update.effective_chat.id, context.chat_data.pop('last_keyboard_message')
        )
    context.chat_data.clear()
    context.user_data.clear()
    product_id = utils.extract_unique_code(update.effective_message.text)
    if product_id:
        context.user_data['product_id'] = product_id
    async with session() as s:
        if await services.CustomerService(s).get_customer(update.effective_chat.id):
            return await post_start(update, context)
    await update.effective_message.reply_text(
        localization.request_inst, reply_markup=markups.skip_markup
    )
    return INST


async def post_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('product_id'):
        return await check_address(update, context, product_id=context.user_data.pop('product_id'))
    else:
        message_data = {
            'text': localization.welcome_message,
            'reply_markup': markups.welcome_markup,
            'parse_mode': ParseMode.MARKDOWN,
        }
        if update.callback_query:
            await update.effective_message.edit_text(**message_data)
        else:
            await update.effective_message.reply_text(**message_data)
        return ConversationHandler.END


async def save_inst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with session() as s:
        await services.CustomerService(s).create(
            schemas.CreateCustomerSchema(
                telegram_chat_id=str(update.effective_chat.id),
                instagram=update.effective_message.text,
                username=update.effective_chat.username,
            )
        )
    return await post_start(update, context)


async def skip_inst(update: Update, context: ContextTypes.DEFAULT_TYPE):
    async with session() as s:
        await services.CustomerService(s).create(
            schemas.CreateCustomerSchema(
                telegram_chat_id=str(update.effective_chat.id),
                username=update.effective_chat.username,
            )
        )
    return await post_start(update, context)


start_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={INST: [MessageHandler(filters.TEXT, save_inst)]},
    fallbacks=[CallbackQueryHandler(skip_inst, callbacks.skip)],
)
