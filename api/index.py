import os
import logging
import random
import asyncio
from flask import Flask, request
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# إعداد Flask
app = Flask(__name__)

# جلب التوكن
TOKEN = os.getenv('BOT_TOKEN')
EMOJI_LIST = ["👏", "😁", "🤔", "🤯", "😱", "🙏", "👌", "🕊️", "🤡", "🥱", "🥴", "😍", "🐳", "🏆", "⚡", "😂", "🌚", "💔", "🤨", "😐", "💋", "😈", "🙈", "👀", "💻", "👻", "🤓", "😭", "😴", "😇", "😰", "🤝", "✍️", "😊", "🫡", "💅", "🤪", "🗿", "🆒", "💘", "👾", "😎", "😉", "😘", "😡", "❤️", "👍", "👎", "🔥", "🥰", "🎉", "😢", "🍓", "💯", "❤️‍🔥"]

# بناء التطبيق مرة واحدة خارج الدالة لتوفير الوقت
tg_app = ApplicationBuilder().token(TOKEN).build()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.chat.type == 'private':
        admin_url = f"https://t.me/Gahkawkwbot?startgroup=true&admin=post_messages+edit_messages+delete_messages+invite_users+pin_messages"
        keyboard = [[InlineKeyboardButton("💎 المطور ↗️", url="https://t.me/theycallmesjd")],
                    [InlineKeyboardButton("🔹 اضفني الى مجموعتك 🔹", url=admin_url)]]
        await update.message.reply_text("<b>بوت تفاعلات تلقائية .</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.chat.type in ['group', 'supergroup']:
        try:
            await update.message.set_reaction(reaction=[ReactionTypeEmoji(emoji=random.choice(EMOJI_LIST))])
        except Exception as e:
            logging.error(f"Reaction Error: {e}")

# إضافة المعالجات (Handlers)
tg_app.add_handler(CommandHandler("start", start_command))
tg_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reaction_handler))

@app.route('/api/index', methods=['POST', 'GET'])
async def webhook():
    if request.method == "POST":
        try:
            # تحويل البيانات القادمة من تلجرام
            update = Update.de_json(request.get_json(force=True), tg_app.bot)
            
            # تشغيل معالجة التحديث بشكل صحيح داخل بيئة Vercel
            async with tg_app:
                await tg_app.process_update(update)
            
            return 'ok', 200
        except Exception as e:
            logging.error(f"Webhook Error: {e}")
            return 'error', 500
    return "Please use POST", 200

@app.route('/')
def home():
    return "Bot is running on Vercel!"
