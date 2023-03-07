import os
from pytube import YouTube
import re
import pytube.exceptions
import time
dir = os.getcwd()


def download_audio(bot, message, url: str):
  try:
    video = YouTube(url)
    if YouTube(url).length > 1800:
      bot.send_message(message.from_user.id, 'Это видео слишком длинное. Допустимая длительность ролика - 30 минут.')
    else:
      name = video.streams[0].title
      name = re.sub('\W -+', '', name)
      name = re.sub(r'[/]', '', name) + '.mp3'

      print(f'[Log] {message.from_user.id} ({message.from_user.first_name}) | request {name} | url: {url}')
      
      t1 = time.time()
      video.streams.get_audio_only().download(filename = name)
      print(f'[LOG] {name} downloaded of {time.time() - t1} seconds.')

      with open(f'{name}', 'rb') as audio:
        bot.send_audio(message.chat.id, audio, reply_to_message_id = message.id, timeout = 10)
      print(f'[Log] {message.from_user.id} ({message.from_user.first_name}) | downloaded {name}')
  except pytube.exceptions.VideoUnavailable:
    bot.send_message(message.from_user.id, 'Видео недоступно.')
  except pytube.exceptions.HTMLParseError:
    bot.send_message(message.from_user.id, 'Введена некорректная ссылка.')
  except pytube.exceptions.RegexMatchError:
    bot.send_message(message.from_user.id, 'Пожалуйста, проверьте, правильно ли вы ввели ссылку.')
  except FileNotFoundError:
    bot.send_message(message.from_user.id, 'Файл не найден на сервере.')
    print(f'[Log: {time.time()}] File not found on server.')
  finally:
    os.remove(os.path.join(dir, name))