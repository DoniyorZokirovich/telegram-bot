from django.conf import settings
from django.core.management import BaseCommand
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from bot.views import start, change_lang, msg_handler, inline_handler, contact_handler, photo_handler


class Command(BaseCommand):
    def handle(self, *args, **options):
        updater = Updater(settings.TOKEN)

        updater.dispatcher.add_handler(CommandHandler('start', start))
        updater.dispatcher.add_handler(CommandHandler('lang', change_lang))



        updater.dispatcher.add_handler(MessageHandler(Filters.text, msg_handler))
        updater.dispatcher.add_handler(MessageHandler(Filters.contact, contact_handler))
        updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
        updater.dispatcher.add_handler(CallbackQueryHandler(inline_handler))

        updater.start_polling()
        updater.idle()