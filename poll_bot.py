import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------------- CONFIG ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set this in Railway environment
# ----------------------------------------

# Per-chat/thread storage (optional, but keeps per-chat flexibility)
group_other_options = {}
group_other_questions = {}

# Default options/question
DEFAULT_OTHER_OPTIONS = [
    "(descript1)",
    "(descript2)",
    "(descript3)"
]
DEFAULT_OTHER_QUESTION = "Other Events"

# ---------- Helpers ----------
def get_options(chat_id):
    return group_other_options.get(chat_id, DEFAULT_OTHER_OPTIONS)

def get_question(chat_id):
    return group_other_questions.get(chat_id, DEFAULT_OTHER_QUESTION)

# ---------- Poll Command ----------
async def poll_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    thread_id = getattr(update.message, "message_thread_id", None)
    question = get_question(chat_id)
    options = get_options(chat_id)

    await context.bot.send_poll(
        chat_id=chat_id,
        message_thread_id=thread_id,
        question=question,
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True
    )

# ---------- Optional /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Other Events Poll Bot ✅ Running 24/7!")

# ---------- Build Bot ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("poll_other", poll_other))

print("Bot started...")
app.run_polling()

