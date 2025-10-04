from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🚨 Token directo (cuidado si el repo es público)
TOKEN = "8298151817:AAFQCZCw2uGQOvDBI55sBpbQucFfzCWICew"

# --- Funciones ---

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Bienvenido!\n\n"
        "Envíame el enlace de tu canal y lo promocionaré aquí mismo 📢."
    )

# Cuando alguien envía un mensaje
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Verifica si parece un link de Telegram
    if text.startswith("https://t.me/") or text.startswith("@"):
        await update.message.reply_text(
            f"✅ Tu canal ha sido promocionado:\n{text}"
        )
    else:
        await update.message.reply_text("❌ Solo acepto enlaces de canales de Telegram.")

# --- Función principal ---
def main():
    app = Application.builder().token(TOKEN).build()

    # Comandos
    app.add_handler(CommandHandler("start", start))

    # Mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()