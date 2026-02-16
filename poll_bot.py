import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------------- CONFIG ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Railway env variable
# ----------------------------------------

# Per-chat/thread storage (optional, separate for each poll)
group_sat_options = {}
group_other_options = {}

# Default poll options
DEFAULT_SAT_OPTIONS = [
    "LUNCH (1230pm) 🍱",
    "I'M COMING (140pm) 🦍",
    "PSA (4pm+) 🐳",
    "CMI (pls state why) 🙁",
    "SERVING 🎸"
]
DEFAULT_OTHER_OPTIONS = [
    "(descript1)",
    "(descript2)",
    "(descript3)"
]

DEFAULT_SAT_QUESTION = "SAT SERVICE⛪️"
DEFAULT_OTHER_QUESTION = "Other Events"

# ---------- Helpers ----------
def get_sat_options(chat_id):
    return group_sat_options.get(chat_id, DEFAULT_SAT_OPTIONS)

def get_other_options(chat_id):
    return group_other_options.get(chat_id, DEFAULT_OTHER_OPTIONS)

# ---------- SAT Poll ----------
async def poll_sat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    thread_id = getattr(update.message, "message_thread_id", None)
    options = get_sat_options(chat_id)
    await context.bot.send_poll(
        chat_id=chat_id,
        message_thread_id=thread_id,
        question=DEFAULT_SAT_QUESTION,
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True
    )

# ---------- Other Events Poll ----------
async def poll_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    thread_id = getattr(update.message, "message_thread_id", None)
    options = get_other_options(chat_id)
    await context.bot.send_poll(
        chat_id=chat_id,
        message_thread_id=thread_id,
        question=DEFAULT_OTHER_QUESTION,
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True
    )

# ---------- Optional /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Poll Bot ✅ Running 24/7!")

# ---------- Build Bot ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("poll_sat", poll_sat))
app.add_handler(CommandHandler("poll_other", poll_other))

print("Bot started...")
app.run_polling()

