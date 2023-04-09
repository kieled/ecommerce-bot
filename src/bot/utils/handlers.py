from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackQueryHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from bot import callbacks, localization
from bot.markups import welcome_markup


async def back_main(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_data = dict(
        text=localization.welcome_message,
        reply_markup=welcome_markup,
        parse_mode=ParseMode.MARKDOWN
    )
    if update.callback_query:
        await update.callback_query.answer()
        await update.effective_message.edit_text(
            **message_data
        )
    else:
        if context.chat_data.get('last_keyboard_message'):
            await context.bot.delete_message(
                update.effective_chat.id,
                context.chat_data.pop('last_keyboard_message')
            )
        await update.effective_message.reply_text(
            **message_data
        )
    context.chat_data.clear()
    context.user_data.clear()
    return ConversationHandler.END


back_main_handler = CallbackQueryHandler(back_main, callbacks.back_main)
back_main_handler_message = MessageHandler(filters.Regex('На главную'), back_main)
