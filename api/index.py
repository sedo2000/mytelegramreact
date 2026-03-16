import os
import asyncio
import random
from flask import Flask, request
from telegram import Update, ReactionTypeEmoji
from telegram.ext import ApplicationBuilder, MessageHandler, filters

app = Flask(__name__)
TOKEN = "8270945505:AAGBeMBqvEp2RhDLCTCAMurChwWimceCt84"
EMOJIS = ["👏", "😁", "🤔", "🤯", "😱", "🙏", "👌", "🕊️", "🤡", "🥱", "🥴", "😍", "🐳", "🏆", "⚡", "😂", "🌚", "💔", "🤨", "😐", "💋", "😈", "🙈", "👀", "💻", "👻", "🤓", "😭", "😴", "😇", "😰", "🤝", "✍️", "😊", "🫡", "💅", "🤪", "🗿", "🆒", "💘", "👾", "😎", "😉", "😘", "😡", "❤️", "👍", "👎", "🔥", "🥰", "🎉", "😢", "🍓", "💯", "❤️‍🔥"]

tg_app = ApplicationBuilder().token(TOKEN).build()

async def react(update: Update, context):
    if update.effective_message and update.effective_chat.type in ['group', 'supergroup']:
        try:
            await update.effective_message.set_reaction(reaction=[ReactionTypeEmoji(emoji=random.choice(EMOJIS))])
        except: pass

tg_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, react))

@app.route('/api/index', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def webhook():
    if request.method == "POST":
        update = Update.de_json(request.get_json(force=True), tg_app.bot)
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(tg_app.initialize())
        loop.run_until_complete(tg_app.process_update(update))
        return 'ok', 200
    # هذا الرد للـ Cron-job ليبقيه مستيقظاً
    return "Bot is awake and ready!", 200
