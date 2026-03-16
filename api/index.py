import os
import asyncio
from flask import Flask, request
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

app = Flask(__name__)

# جلب التوكن مع وضع قيمة افتراضية للتأكد من عدم حدوث Error 500 بسبب التوكن
TOKEN = os.getenv('BOT_TOKEN', '8270945505:AAGBeMBqvEp2RhDLCTCAMurChwWimceCt84')

EMOJI_LIST = ["👏", "😁", "🤔", "🤯", "😱", "🙏", "👌", "🕊️", "🤡", "🥱", "🥴", "😍", "🐳", "🏆", "⚡", "😂", "🌚", "💔", "🤨", "😐", "💋", "😈", "🙈", "👀", "💻", "👻", "🤓", "😭", "😴", "😇", "😰", "🤝", "✍️", "😊", "🫡", "💅", "🤪", "🗿", "🆒", "💘", "👾", "😎", "😉", "😘", "😡", "❤️", "👍", "👎", "🔥", "🥰", "🎉", "😢", "🍓", "💯", "❤️‍🔥"]

# تعريف التطبيق
tg_app = ApplicationBuilder().token(TOKEN).build()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        keyboard = [[InlineKeyboardButton("💎 المطور ↗️", url="https://t.me/theycallmesjd")]]
        await update.message.reply_text("<b>البوت يعمل بنجاح على فيرسل!</b>", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='HTML')

async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.chat.type in ['group', 'supergroup']:
        try:
            import random
            await update.message.set_reaction(reaction=[ReactionTypeEmoji(emoji=random.choice(EMOJI_LIST))])
        except:
            pass

tg_app.add_handler(CommandHandler("start", start_command))
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
            print(f"Error: {e}")
            return str(e), 500
    return "OK", 200
