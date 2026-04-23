import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import yt_dlp
import os
import base64
from flask import Flask
from threading import Thread

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

# ================== KEEP ALIVE SERVER ==================
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ================== START COMMAND ==================
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()

    markup.add(
        InlineKeyboardButton("📢 SUBSCRIBE CHANNEL", url=YOUTUBE_LINK)
    )
    markup.add(
        InlineKeyboardButton("🎬 ALL TUTORIALS", url=YOUTUBE_LINK)
    )
    markup.add(
        InlineKeyboardButton("👤 CONTACT OWNER", url=SUPPORT_LINK)
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

        # Update status
        bot.edit_message_text(
            "⬇️ Downloading... (50%)",
            message.chat.id,
            status_msg.message_id
        )

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        # Update status
        bot.edit_message_text(
            "📤 Uploading... (100%)",
            message.chat.id,
            status_msg.message_id
        )

        # Send video
        with open(file_path, 'rb') as video:
            bot.send_video(
                message.chat.id,
                video,
                caption="Downloaded Successfully!\nPower by: @Facebook_video_Downloaderr_bot"
            )

        # Cleanup
        os.remove(file_path)

        # Final status update
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

# ================== MAIN ==================
if __name__ == "__main__":
    keep_alive()
    print("Bot is running...")
    bot.infinity_polling()
