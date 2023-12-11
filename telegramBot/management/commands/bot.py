from django.core.management.base import BaseCommand
from django.conf import settings

from telebot import TeleBot

# from config import *
#
# from telegram.utils.request import Request
# from telegram import Bot


# Название класса обязательно - "Command"
class Command(BaseCommand):
  	# Используется как описание команды обычно
    help = 'Telegram bot.'

    def handle(self, *args, **kwargs):
        pass