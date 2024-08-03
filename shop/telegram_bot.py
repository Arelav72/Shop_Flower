from telegram import Bot, Update
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from django.conf import settings
from django.core.management.base import BaseCommand

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

def start(update, context):
    update.message.reply_text('Привет! Я бот для магазина цветов.')

def handle_order(update, context):
    # Здесь получаем информацию о заказе и отправляем сообщение
    order_info = "Информация о заказе: ...\nИзображение: ...\nСтоимость: ...\nДата и время: ...\nМесто доставки: ...\нКомментарий: ..."
    update.message.reply_text(order_info)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_order))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
