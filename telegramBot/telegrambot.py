# # ваше_приложение/telegrambot.py
# from django_telegrambot.apps import DjangoTelegramBot
# from telegram import Update
# from telegram.ext import CallbackContext
#
# def start_command(update: Update, context: CallbackContext):
#     user = update.message.from_user
#     message_text = f"Привет, {user.first_name}! Добро пожаловать! Я ваш телеграм-бот в Django."
#     update.message.reply_text(message_text)
#
# # Получите экземпляр бота
# bot = DjangoTelegramBot.get_bot()
#
# # Добавьте обработчик команды /start
# bot.add_message_handler(start_command, commands=['start'])
