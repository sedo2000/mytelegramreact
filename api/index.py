import os
import asyncio
import random
from flask import Flask, request
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

app = Flask(__name__)

TOKEN = os.getenv('BOT_TOKEN', '8270945505:AAGBeMBqvEp2RhDLCTCAMurChwWimceCt84')
EMOJI_LIST = ["👏", "😁", "🤔", "🤯", "😱", "🙏", "👌", "🕊️", "🤡", "🥱", "🥴", "😍", "🐳", "🏆", "⚡", "😂", "🌚", "💔", "🤨", "😐", "💋", "😈", "🙈", "👀", "💻", "👻", "🤓", "😭", "😴", "😇", "😰", "🤝", "✍️", "😊", "🫡", "💅", "🤪", "🗿", "🆒", "💘", "👾", "😎", "😉", "😘", "😡", "❤️", "👍", "👎", "🔥", "🥰", "🎉", "😢", "🍓", "💯", "❤️‍🔥"]

tg_app = ApplicationBuilder().token(TOKEN).build()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # رابط الإضافة كمشرف مباشرة
    admin_url = f"https://t.me/{context.bot.username}?startgroup=true&admin=post_messages+edit_messages+delete_messages+invite_users+pin_messages"
    
    keyboard = [
        [InlineKeyboardButton("💎 المطور ↗️", url="https://t.me/theycallmesjd")],
        [InlineKeyboardButton("🔹 اضفني الى مجموعتك 🔹", url=admin_url)]
    ]
    await update.message.reply_text(
        "<b>بوت تفاعلات تلقائية يعمل بنجاح!</b>\n\nاضغط على الزر أدناه لإضافتي لمجموعتك.",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التفاعل في المجموعات (للرسائل والوسائط)
    if update.effective_message and update.effective_chat.type in ['group', 'supergroup']:
        try:
            await update.effective_message.set_reaction(reaction=[ReactionTypeEmoji(emoji=random.choice(EMOJI_LIST))])
        except Exception as e:
            print(f"Reaction Error: {e}")

# إضافة المعالجات
tg_app.add_handler(CommandHandler("start", start_command))
# تم تغيير الفلتر إلى ALL ليشمل الصور والرسائل والملفات
tg_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reaction_handler))

@app.route('/', methods=['POST', 'GET'])
@app.route('/api/index', methods=['POST', 'GET'])
def webhook():
    if request.method == "POST":
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            update = Update.de_json(request.get_json(force=True), tg_app.bot)
            loop.run_until_complete(tg_app.initialize())
            loop.run_until_complete(tg_app.process_update(update))
            return 'ok', 200
        except Exception as e:
            return str(e), 500
    return "Bot is Active!", 200
