import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# ---------------- CONFIG ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Set this in Railway environment
# ----------------------------------------

# Per-chat/thread storage
group_sat_options = {}
group_other_options = {}
group_other_questions = {}

# Default SAT poll
DEFAULT_SAT_OPTIONS = [
    "LUNCH (1230pm) 🍱",
    "I'M COMING (140pm) 🦍",
    "PSA (4pm+) 🐳",
    "CMI (pls state why) 🙁",
    "SERVING 🎸"
]
DEFAULT_SAT_QUESTION = "SAT SERVICE⛪️"

# Default Other poll
DEFAULT_OTHER_OPTIONS = [
    "(descript1)",
    "(descript2)",
    "(descript3)"
]
DEFAULT_OTHER_QUESTION = "Other Events"

# ---------- Helpers ----------
def get_sat_options(chat_id):
    return group_sat_options.get(chat_id, DEFAULT_SAT_OPTIONS)

def get_other_options(chat_id):
    return group_other_options.get(chat_id, DEFAULT_OTHER_OPTIONS)

def get_other_question(chat_id):
    return group_other_questions.get(chat_id, DEFAULT_OTHER_QUESTION)

# ---------- SAT Poll ----------
async def pollsat(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
async def pollother(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    thread_id = getattr(update.message, "message_thread_id", None)
    options = get_other_options(chat_id)
    question = get_other_question(chat_id)

    await context.bot.send_poll(
        chat_id=chat_id,
        message_thread_id=thread_id,
        question=question,
        options=options,
        is_anonymous=False,
        allows_multiple_answers=True
    )

# ---------- Set SAT Poll Options ----------
async def setsat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: /setsat option1 | option2 | option3")
        return
    group_sat_options[chat_id] = [opt.strip() for opt in text.split("|") if opt.strip()]
    await update.message.reply_text(f"✅ SAT poll options updated:\n{group_sat_options[chat_id]}")

# ---------- Set Other Poll Options ----------
async def setother(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: /setother option1 | option2 | option3")
        return
    group_other_options[chat_id] = [opt.strip() for opt in text.split("|") if opt.strip()]
    await update.message.reply_text(f"✅ Other poll options updated:\n{group_other_options[chat_id]}")

# ---------- Set Other Poll Question ----------
async def setquestionother(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Usage: /setquestionother Your new poll question")
        return
    group_other_questions[chat_id] = text
    await update.message.reply_text(f"✅ Other Events poll question updated:\n{text}")

# ---------- Optional /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Poll Bot ✅ Running 24/7!")

# ---------- Build Bot ----------
app = ApplicationBuilder().token(BOT_TOKEN).build()

# Add handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("pollsat", pollsat))
app.add_handler(CommandHandler("pollother", pollother))
app.add_handler(CommandHandler("setsat", setsat))
app.add_handler(CommandHandler("setother", setother))
app.add_handler(CommandHandler("setquestionother", setquestionother))

print("Bot started...")
app.run_polling()



