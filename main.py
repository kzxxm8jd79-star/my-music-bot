import telebot
import os
from yt_dlp import YoutubeDL

TOKEN = '8759955362:AAGDM4YF0oYFvxgvPzzxItpudO7w3Ze3NTI' # Твой токен
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Пришли название песни, и я пришлю тебе аудиофайл прямо сюда.")

@bot.message_handler(func=lambda message: True)
def download_and_send(message):
    msg = bot.send_message(message.chat.id, "⏳ Скачиваю аудио... подожди немного.")
    
    # Настройки для скачивания только звука в лучшем качестве
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'song.mp3', # Сохраняем как song.mp3
        'noplaylist': True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            # Ищем и скачиваем файл
            info = ydl.extract_info(f"ytsearch:{message.text}", download=True)['entries'][0]
            title = info.get('title', 'music')
            
        # Отправляем файл в Telegram
        with open('song.mp3', 'rb') as audio:
            bot.send_audio(message.chat.id, audio, title=title)
        
        # Удаляем файл с сервера, чтобы не занимать место
        os.remove('song.mp3')
        bot.delete_message(message.chat.id, msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"❌ Ошибка: Не удалось загрузить песню.", message.chat.id, msg.message_id)
        if os.path.exists('song.mp3'):
            os.remove('song.mp3')

bot.infinity_polling()
