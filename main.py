import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import os
import base64

# ================== CONFIG ==================
BOT_TOKEN = "8621986845:AAE-iTAWwH0aTQKX_6np6JIB_mfVU7HhfXM"
bot = telebot.TeleBot(BOT_TOKEN)

# Decode secured links
YOUTUBE_LINK = base64.b64decode(
    "aHR0cHM6Ly95b3V0dWJlLmNvbS9AYmxhY2trbm93bGVkZ2VfMTkwP3NpPTlFd2tNUEdiLWxIUnpaZHE="
).decode("utf-8")

SUPPORT_LINK = base64.b64decode(
    "aHR0cHM6Ly90Lm1lL0JMQUNLX0tub3dsZWRnZV8xOTA="
).decode("utf-8")

# ================== START COMMAND ==================
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("📢 SUBSCRIBE CHANNEL", url="https://t.me/CreativeSpark1")
    )
    markup.add(
        InlineKeyboardButton("🎬 ALL TUTORIALS", url=YOUTUBE_LINK)
    )
    markup.add(
        InlineKeyboardButton("👤 CONTACT OWNER", url="https://t.me/ShahriarRazz143")
    )

    welcome_text = """
🔥 *Welcome to Facebook & Instagram Video Downloader Bot!*

🚀 *Bot Name:* @Facebook_video_Downloaderr_bot  
🎯 Download Videos from:
• Facebook  
• Instagram Reels  

⚡ Fast | Reliable | High Quality  

📌 Just send a video link and let the magic happen!
"""

    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="Markdown",
        reply_markup=markup
    )

# ================== DOWNLOAD HANDLER ==================
@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text.strip()

    status_msg = bot.reply_to(message, "🔍 Analyzing...")

    try:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'best',
            'noplaylist': True,
            'quiet': True
        }

        bot.edit_message_text(
            "⬇️ Downloading... (50%)",
            message.chat.id,
            status_msg.message_id
        )

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        bot.edit_message_text(
            "📤 Uploading... (100%)",
            message.chat.id,
            status_msg.message_id
        )

        with open(file_path, 'rb') as video:
            bot.send_video(
                message.chat.id,
                video,
                caption="Downloaded Successfully!\nPower by: @Facebook_video_Downloaderr_bot"
            )

        os.remove(file_path)

        bot.edit_message_text(
            "✅ Done!",
            message.chat.id,
            status_msg.message_id
        )

    except Exception as e:
        bot.edit_message_text(
            f"❌ Error: {str(e)}",
            message.chat.id,
            status_msg.message_id
        )

# ================== MAIN (RENDER FIX) ==================
if __name__ == "__main__":
    print("Bot is running...")

    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
