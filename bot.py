import logging
import random
import os
from flask import Flask, request
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# إعداد السجلات
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# التوكن
TOKEN = '8270945505:AAGBeMBqvEp2RhDLCTCAMurChwWimceCt84'

# قائمة التفاعلات
EMOJI_LIST = [
    "👏", "😁", "🤔", "🤯", "😱", "🙏", "👌", "🕊️", "🤡", "🥱", "🥴",
    "😍", "🐳", "🏆", "⚡", "😂", "🌭", "🌚", "💔", "🤨", "😐", "🍾",
    "💋", "😈", "🙈", "🎃", "👀", "💻", "👻", "🤓", "😭", "😴", "😇",
    "😰", "🤝", "✍️", "😊", "🫡", "🎅", "🎄", "☃️", "💅", "🤪", "🗿",
    "🆒", "💘", "🙊", "🦄", "🤷‍♀️", "🤷‍♂️", "🤷", "👾", "😎", "😉", "💊",
    "😘", "😡", "❤️", "👍", "👎", "🔥", "🥰", "🎉", "😢", "💯", "❤️‍🔥"
]

# إعداد Flask
app = Flask(__name__)

# بناء تطبيق التلجرام (بدون تشغيل Polling)
tg_app = ApplicationBuilder().token(TOKEN).build()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat.type == 'private':
        admin_url = "https://t.me/Gahkawkwbot?startgroup=true&admin=post_messages+edit_messages+delete_messages+invite_users+pin_messages"
        keyboard = [
            [InlineKeyboardButton("المطور ↗️", url="https://t.me/theycallmesjd")],
            [InlineKeyboardButton("اضفني الى مجموعتك ➕", url=admin_url)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("بوت تفاعلات تلقائية .", reply_markup=reply_markup)

async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.chat.type in ['group', 'supergroup']:
        try:
            random_emoji = random.choice(EMOJI_LIST)
            await update.message.set_reaction(reaction=[ReactionTypeEmoji(emoji=random_emoji)])
        except:
            try:
                await update.message.set_reaction(reaction=[ReactionTypeEmoji(emoji="❤️")])
            except: pass

# إضافة المعالجات
tg_app.add_handler(CommandHandler("start", start_command))
tg_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reaction_handler))

# المسار الذي سيرسل عليه تلجرام البيانات (Webhook Endpoint)
@app.route('/' + TOKEN, methods=['POST'])
async def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), tg_app.bot)
        await tg_app.initialize()
        await tg_app.process_update(update)
        return 'ok', 200

@app.route('/')
def index():
    return "Bot is Running!"

if __name__ == '__main__':
    # ملاحظة: عند الرفع للاستضافة، الاستضافة هي من تشغل التطبيق عبر Gunicorn أو محرك ويب
    app.run(port=int(os.environ.get('PORT', 5000)))
