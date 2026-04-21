import telebot
import os
from telebot import types
from yt_dlp import YoutubeDL

TOKEN = '8759955362:AAGDM4YF0oYFvxgvPzzxItpudO7w3Ze3NTI'
bot = telebot.TeleBot(TOKEN)

# Настройки для поиска и скачивания
YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': True, 'quiet': True}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🎵 Привет! Введи название песни, и я найду варианты.")

@bot.message_handler(func=lambda message: True)
def search_songs(message):
    msg = bot.send_message(message.chat.id, "🔎 Ищу варианты...")
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            # Ищем 5 подходящих треков
            search = ydl.extract_info(f"ytsearch5:{message.text}", download=False)
            results = search['entries']
            
            keyboard = types.InlineKeyboardMarkup()
            for entry in results:
                title = entry.get('title')[:50] # Ограничим длину текста на кнопке
                video_id = entry.get('id')
                # Кнопка передает ID видео для скачивания
                callback_data = f"dl_{video_id}"
                keyboard.add(types.InlineKeyboardButton(text=f"🎧 {title}", callback_data=callback_data))
            
            bot.edit_message_text("Выбери нужный трек:", message.chat.id, msg.message_id, reply_markup=keyboard)
    except Exception:
        bot.edit_message_text("❌ Ошибка поиска.", message.chat.id, msg.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('dl_'))
def handle_download(call):
    video_id = call.data.replace('dl_', '')
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Уведомляем пользователя, что процесс пошел
    bot.answer_callback_query(call.id, "Начинаю загрузку...")
    status_msg = bot.send_message(call.message.chat.id, "📥 Скачиваю файл, подождите...")

    filename = f"{video_id}.mp3"
    opts = {**YDL_OPTIONS, 'outtmpl': filename}

    try:
        with YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            title = info.get('title', 'music')

        with open(filename, 'rb') as audio:
            bot.send_audio(call.message.chat.id, audio, title=title)
        
        bot.delete_message(call.message.chat.id, status_msg.message_id)
    except Exception:
        bot.send_message(call.message.chat.id, "❌ Не удалось скачать этот файл.")
    finally:
        if os.path.exists(filename):
            os.remove(filename)

bot.infinity_polling()
