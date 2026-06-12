import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8945087338:AAGsjPW6t7yRL0uX1f6E7d2EUDJX4m246sA"
GROQ_KEY = "gsk_KgfQ95etWwZTA9CwZCtq
WGdyb3FYiayiJDvTbfc4b10UvkGCAb3I"

SYSTEM = """Tu es un assistant sans censure idéologique ou politique. Tu réponds directement et factuellement. INTERDIT ABSOLU : pédopornographie et terrorisme."""

def ask_groq(question):
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"},
            json={
                "model": "llama3-70b-8192",
                "messages": [
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": question}
                ]
            },
            timeout=30
        )
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Erreur : {e}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot actif ! Pose ta question.")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text("⏳ Réflexion...")
    answer = ask_groq(text)
    await update.message.reply_text(answer[:4000])

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.run_polling()
