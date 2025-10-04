from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🚨 Token directo (cuidado si tu repo es público en GitHub)
TOKEN = "8298151817:AAFQCZCw2uGQOvDBI55sBpbQucFfzCWICew"

# Lista de botones de canales
channels = [
    {"name": "🔥 Canal Oficial", "url": "https://t.me/TU_CANAL"}  # <-- cambia por el tuyo
]

# --- Funciones ---

# Construir teclado dinámico
def build_keyboard():
    keyboard = []
    for ch in channels:
        keyboard.append([InlineKeyboardButton(ch["name"], url=ch["url"])])
    return InlineKeyboardMarkup(keyboard)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📢 Bienvenido!\n\nAquí puedes ver canales promocionados o enviar el tuyo 👇",
        reply_markup=build_keyboard()
    )

# Usuario manda un link
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    # Aceptar solo links de Telegram
    if text.startswith("https://t.me/") or text.startswith("@"):
        new_channel = {"name": f"Canal de {update.effective_user.first_name}", "url": text}
        channels.append(new_channel)

        await update.message.reply_text(
            "✅ Tu canal ha sido añadido a la lista de promoción.",
            reply_markup=build_keyboard()
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