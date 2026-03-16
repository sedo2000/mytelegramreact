import os
import asyncio
import random
from flask import Flask, request
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

app = Flask(__name__)

# وضع التوكن مباشرة يسرع العملية قليلاً بدلاً من البحث في ملفات البيئة في كل مرة
TOKEN = "8270945505:AAGBeMBqvEp2RhDLCTCAMurChwWimceCt84"
EMOJIS = ["👏", "😁", "🤔", "🤯", "😱", "🙏", "👌", "🕊️", "🤡", "🥱", "🥴", "😍", "🐳", "🏆", "⚡", "😂", "🌚", "💔", "🤨", "😐", "💋", "😈", "🙈", "👀", "💻", "👻", "🤓", "😭", "😴", "😇", "😰", "🤝", "✍️", "😊", "🫡", "💅", "🤪", "🗿", "🆒", "💘", "👾", "😎", "😉", "😘", "😡", "❤️", "👍", "👎", "🔥", "🥰", "🎉", "😢", "🍓", "💯", "❤️‍🔥"]

# إنشاء التطبيق مرة واحدة عند التشغيل (Global Variable)
tg_app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context):
    user_id = update.effective_user.id
    admin_url = f"https://t.me/Gahkawkwbot?startgroup=true&admin=post_messages+edit_messages+delete_messages+invite_users+pin_messages"
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 المطور ↗️", url="https://t.me/theycallmesjd")],
        [InlineKeyboardButton("🔹 اضفني الى مجموعتك 🔹", url=admin_url)]
    ])
    await update.message.reply_text("<b>بوت تفاعلات تلقائية سريع ⚡</b>", reply_markup=keyboard, parse_mode='HTML')

async def react(update: Update, context):
    if update.effective_message and update.effective_chat.type in ['group', 'supergroup']:
        try:
            # استخدام أسرع طريقة لإرسال التفاعل دون معالجة إضافية
            await update.effective_message.set_reaction(reaction=[ReactionTypeEmoji(emoji=random.choice(EMOJIS))])
        except:
            pass

tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, react))

@app.route('/api/index', methods=['POST', 'GET'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), tg_app.bot)
        # استخدام حلقة الأحداث الحالية بدلاً من إنشاء واحدة جديدة في كل مرة لتوفير الوقت
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(tg_app.initialize())
        loop.run_until_complete(tg_app.process_update(update))
        return 'ok', 200
    return "Fast Bot is Running!", 200
