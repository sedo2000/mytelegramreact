import os
import asyncio
import random
import logging
from flask import Flask, request
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# إعداد Flask
app = Flask(__name__)

# جلب التوكن (تأكد أنه مضاف في Vercel Environment Variables)
TOKEN = os.getenv('BOT_TOKEN', '8270945505:AAGBeMBqvEp2RhDLCTCAMurChwWimceCt84')

# قائمة الإيموجي الشاملة للتفاعل
EMOJI_LIST = ["👏", "😁", "🤔", "🤯", "😱", "🙏", "👌", "🕊️", "🤡", "🥱", "🥴", "😍", "🐳", "🏆", "⚡", "😂", "🌚", "💔", "🤨", "😐", "💋", "😈", "🙈", "👀", "💻", "👻", "🤓", "😭", "😴", "😇", "😰", "🤝", "✍️", "😊", "🫡", "💅", "🤪", "🗿", "🆒", "💘", "👾", "😎", "😉", "😘", "😡", "❤️", "👍", "👎", "🔥", "🥰", "🎉", "😢", "🍓", "💯", "❤️‍🔥"]

# بناء التطبيق
tg_app = ApplicationBuilder().token(TOKEN).build()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج أمر /start لإظهار أزرار المطور والإضافة"""
    bot_username = (await context.bot.get_me()).username
    admin_url = f"https://t.me/{bot_username}?startgroup=true&admin=post_messages+edit_messages+delete_messages+invite_users+pin_messages"
    
    keyboard = [
        [InlineKeyboardButton("💎 المطور ↗️", url="https://t.me/theycallmesjd")],
        [InlineKeyboardButton("🔹 اضفني الى مجموعتك 🔹", url=admin_url)]
    ]
    
    await update.message.reply_text(
        "<b>أهلاً بك في بوت التفاعلات التلقائية! 🤖</b>\n\n"
        "✅ أتفاعل مع الرسائل، الصور، الفيديوهات، والملصقات.\n"
        "✅ أعمل في المجموعات والقنوات والخاص.\n\n"
        "<b>اضغط على الزر أدناه لإضافتي لمجموعتك مباشرة:</b>",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='HTML'
    )

async def reaction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """معالج التفاعلات الشامل للمجموعات"""
    # التحقق من أن التحديث يحتوي على رسالة وأنها في مجموعة
    message = update.effective_message
    chat = update.effective_chat
    
    if message and chat and chat.type in ['group', 'supergroup']:
        try:
            # اختيار إيموجي عشوائي وإرسال التفاعل
            selected_emoji = random.choice(EMOJI_LIST)
            await message.set_reaction(reaction=[ReactionTypeEmoji(emoji=selected_emoji)])
        except Exception as e:
            logging.error(f"خطأ في التفاعل: {e}")

# إضافة المعالجات للتطبيق
tg_app.add_handler(CommandHandler("start", start_command))
# الفلتر ALL يضمن التقاط (النصوص، الصور، الفيديو، المستندات، الملصقات)
tg_app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, reaction_handler))

@app.route('/', methods=['POST', 'GET'])
@app.route('/api/index', methods=['POST', 'GET'])
def webhook():
    """المسار الذي يستقبل تحديثات تلجرام على Vercel"""
    if request.method == "POST":
        try:
            # إنشاء حلقة أحداث جديدة لكل طلب (ضروري لبيئة Serverless)
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # تحويل البيانات القادمة إلى كائن Update
            update = Update.de_json(request.get_json(force=True), tg_app.bot)
            
            # تشغيل المعالجة
            loop.run_until_complete(tg_app.initialize())
            loop.run_until_complete(tg_app.process_update(update))
            loop.close()
            
            return 'ok', 200
        except Exception as e:
            logging.error(f"Webhook Error: {e}")
            return str(e), 500
            
    return "<h1>Bot Status: Running ✅</h1>", 200
