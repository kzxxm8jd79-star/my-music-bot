import telebot
from yt_dlp import YoutubeDL

# Вставь сюда свой токен от BotFather
TOKEN = '8759955362:AAGDM4YFOoYFvxgvPzzxItpudO7w3Ze3NTI'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Пришли мне название песни, и я попробую найти её!")

@bot.message_handler(func=lambda message: True)
def search_music(message):
    msg = bot.send_message(message.chat.id, "🔍 Ищу... подожди немного.")
    try:
        with YoutubeDL({'format': 'bestaudio', 'noplaylist': True}) as ydl:
            info = ydl.extract_info(f"ytsearch:{message.text}", download=False)['entries'][0]
            url = info['url']
            title = info['title']
            bot.edit_message_text(f"✅ Нашел: {title}\n🔗 Ссылка: {url}", message.chat.id, msg.message_id)
    except Exception as e:
        bot.edit_message_text("❌ Ничего не нашлось. Попробуй другое название.", message.chat.id, msg.message_id)

bot.infinity_polling()
