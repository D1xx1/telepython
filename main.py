from telebot import TeleBot

from utils.audio import download_audio

from cfg.token import telegram_token

import utils.yandex

bot = TeleBot(telegram_token)

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(
    message.chat.id, '''
Привет, я могу скачивать музыку с YouTube
Для этого тебе нужно лишь переслать мне ссылку на любое видео и если не будет никаких проблем, то перешлю тебе аудиофайл.
Попробуй, это легко и просто! Помни, ссылка должна начинаться с 'http'
/help
  ''')

@bot.message_handler(commands = ['help'])
def faq(message):
  bot.send_message(message.from_user.id, 'Для начала стоит найти ролик, аудио или видео которого хочешь скачать. После чего, на странице ролика нажми "Поделиться" и "Скопировать ссылку", после чего отправь её мне и выбери, что нужно скачать. Помни, длительность ролика не должна превышать 30 минут.')

@bot.message_handler(regexp='http')
def sendMedia(message):
  download_audio(bot, message, url=message.text)

@bot.message_handler(commands=['shutdown','status'])
def shutdown(message):
  if message.from_user.id == 1321604362 and message.text == '/shutdown':
    bot.send_message(1321604362, 'Shutdown?')
    bot.register_next_step_handler_by_chat_id(1321604362, shutdown)
  if message.from_user.id == 1321604362 and message.text == '/status':
    bot.send_message(1321604362, 'Working')

def shutdown(message):
  if message.from_user.id == 1321604362 and message.text == 'yes':
    bot.stop_bot()
  else:
    bot.register_next_step_handler_by_chat_id(1321604362, sendMedia)
    

if __name__ == '__main__':
  bot.infinity_polling(timeout=90, long_polling_timeout=90)