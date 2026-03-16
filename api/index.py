import os
import asyncio
import random
import logging
from flask import Flask, request
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# إعداد Flask
app = Flask(__name__)

# التوكن
TOKEN = "8270945505:AAGBeMBqvEp2RhDLCTCAMurChwWimceCt84"

# قائمة الإيموجي
EMOJI_LIST = ["👏", "😁", "🤔", "🤯", "😱", "🙏", "👌", "🕊️", "🤡", "🥱", "🥴", "😍", "🐳", "🏆", "⚡", "😂", "🌚", "💔", "🤨", "😐", "💋", "😈", "🙈", "👀", "💻", "👻", "🤓", "😭", "😴", "😇", "😰", "🤝", "✍️", "😊", "🫡", "💅", "🤪", "🗿", "🆒", "💘", "👾", "😎", "😉", "😘", "😡", "❤️", "👍", "👎", "🔥", "🥰", "🎉", "😢", "🍓", "💯", "❤️‍🔥"]

# بناء التطبيق
tg_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    admin_url = f"https://t.me/Gahkawkwbot?startgroup=true&admin=post_messages+edit_messages+delete_messages+invite_users+pin_messages"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(" المطور ", url="https://t.me/theycallmesjd")],
        [InlineKeyboardButton("اضفني الى مجموعتك ", url=admin_url)]
    ])
    await update.message.reply_text("<b>بوت التفاعلات التلقائية ⚡</b>\n\nأرسل أي رسالة أو وسائط في المجموعة وسأقوم بالتفاعل!", reply_markup=keyboard, parse_mode='HTML')

async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_message and update.effective_chat.type in ['group', 'supergroup']:
        try:
            await update.effective_message.set_reaction(reaction=[ReactionTypeEmoji(emoji=random.choice(EMOJI_LIST))])
        except:
            pass

# إضافة المعالجات
tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reaction_handler))

# دالة الويب هوك والـ Cron المدمجة
@app.route('/', methods=['POST', 'GET'])
@app.route('/api/index', methods=['POST', 'GET'])
def webhook():
    if request.method == "POST":
        try:
            # معالجة بيانات تلجرام
            update = Update.de_json(request.get_json(force=True), tg_app.bot)
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(tg_app.initialize())
            loop.run_until_complete(tg_app.process_update(update))
            loop.close()
            
            return 'ok', 200
        except Exception as e:
            logging.error(f"Error: {e}")
            return 'ok', 200 # نرد بـ OK دائماً لتجنب التكرار
            
    # هذا السطر مخصص لـ Cron-job لإبقاء السيرفر مستيقظاً (عند طلب GET)
    return "Bot is Awake!", 200
