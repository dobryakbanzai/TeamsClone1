from django.core.management.base import BaseCommand
from telegram_bot import *
from telegram_bot import telegram_bot


# Название класса обязательно - "Command"
class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Telegram bot.'

    def handle(self, *args, **kwargs):
        telegram_bot.start_bot()