from telegram.ext import ApplicationBuilder
from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

from bot import handlers, utils
from config import settings


def build():
    filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

    app = ApplicationBuilder().token(settings.TG_BOT_TOKEN).build()

    app.add_handler(handlers.start_handler)
    app.add_handler(handlers.find_handler)
    app.add_handler(handlers.buy_handler)
    app.add_handler(handlers.product_handler)

    app.add_handler(utils.back_main_handler)
    app.add_handler(utils.back_main_handler_message)

    return app
