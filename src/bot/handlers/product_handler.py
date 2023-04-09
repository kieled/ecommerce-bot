import io
import json
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import (
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)
from bot import callbacks, utils, localization, schemas, services, markups
from db import session

PAYMENT, CHECK = range(2)


async def product_web_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data

    if not data['product_id'] or not data['price']:
        return
    if context.chat_data['last_keyboard_message']:
        await context.bot.delete_message(
            update.effective_chat.id, context.chat_data.pop('last_keyboard_message')
        )
    await update.effective_message.delete()
    data = json.loads(update.effective_message.web_app_data.data)
    context.user_data.update(data.items())
    async with session() as s:
        requisite = await services.RequisiteService(s).get_active()
    await update.message.reply_markdown(
        text=localization.product_payout_message(requisite, context.user_data.get('price')),
        reply_markup=markups.product_payout_markup,
    )
    context.user_data['requisite_id'] = requisite.id
    return PAYMENT


async def product_payment(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.effective_message.reply_text(
        localization.send_check_message, reply_markup=ReplyKeyboardRemove()
    )
    return CHECK


async def check_receive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data

    async with session() as s:
        customer_id: int = (
            await services.CustomerService(s).get_customer(update.effective_chat.id)
        ).id

        transaction_id = await services.TransactionService(s).create(
            schemas.CreateTransactionSchema(
                amount=data.get('price'),
                customer_id=customer_id,
                requisite_id=data.pop('requisite_id'),
            )
        )
        if not data.get('address_id'):
            data['address_id'] = await services.CustomerService(s).add_address(
                schemas.CreateAddressSchema(
                    address=data.get('address'),
                    city=data.pop('city'),
                    country=data.pop('country'),
                    customer_id=customer_id,
                    first_name=data.pop('first_name'),
                    last_name=data.pop('last_name'),
                    postal_index=data.pop('index'),
                )
            )

    check = io.BytesIO()
    await (
        await context.bot.get_file(update.effective_message.effective_attachment)
    ).download_to_memory(check)
    check_path = await utils.upload_check(transaction_id, check.getvalue())
    check.close()

    async with session() as s:
        await services.TransactionService(s).add_check(
            schemas.AddCheckTransactionSchema(transaction_id=transaction_id, check_path=check_path)
        )
        admins = await services.AdminService(s).get_tg()
        order_id: int = await services.OrderService(s).create(
            schemas.CreateOrderSchema(
                product_id=data.pop('product_id'),
                product_color_id=data.pop('color'),
                product_size_id=data.pop('size') if data.get('size') else None,
                transaction_id=transaction_id,
                customer_address_id=data.pop('address_id'),
            )
        )

    await update.effective_message.reply_text(
        localization.product_complete_message(order_id), reply_markup=markups.back_main_markup
    )

    for admin in admins:
        await context.bot.send_message(
            admin, localization.new_order_message(order_id, data.get('price'))
        )
    return ConversationHandler.END


async def check_failed(update: Update, _: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        localization.not_valid_image, reply_markup=markups.back_main_markup
    )
    return CHECK


product_handler = ConversationHandler(
    entry_points=[MessageHandler(filters.StatusUpdate.WEB_APP_DATA, product_web_data)],
    states={
        PAYMENT: [CallbackQueryHandler(product_payment, callbacks.paid)],
        CHECK: [
            MessageHandler(filters.Document.IMAGE, check_receive),
            MessageHandler(filters.ALL & ~filters.Document.IMAGE, check_failed),
        ],
    },
    fallbacks=[utils.back_main_handler, utils.back_main_handler_message],
)
