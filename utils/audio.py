import os
from pytube import YouTube
import pytube.exceptions
import time
from utils import yandex, functions
dir = os.getcwd()


def download_audio(bot, message, url: str):
  try:
    video = YouTube(url)
    name = functions.namechanger(video,'.mp3')
    print(f'[Log] {message.from_user.id} ({message.from_user.first_name}) | request {name} | url: {url}')
    t1 = time.time()
    video.streams.get_audio_only().download(filename = name)
    print(f'[LOG] {name} downloaded of {time.time() - t1} seconds.')
    if YouTube(url).streams.get_highest_resolution().filesize > 52428800:
      bot.send_message(message.from_user.id, 'Этот ролик слишком длинный. Файл будет загружен в облако и доступен для скачивания по ссылке.')
      print(f'Start to upload {name} to yadisk...')
      yadisk_url = yandex.uploadToDisk(name)
      print('Upload complete.')
      bot.send_message(message.from_user.id, f'Файл доступен для скачиания по ссылке: {yadisk_url}')
    
    else:
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