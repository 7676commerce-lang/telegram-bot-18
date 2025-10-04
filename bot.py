import os
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

# 🚨 Tu token directo (ojo si tu repo es público)
TOKEN = "8298151817:AAFQCZCw2uGQOvDBI55sBpbQucFfzCWICew"

# Archivo donde guardamos los canales
DATA_FILE = "channels.json"

# --- Cargar / guardar canales ---
def load_channels():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_channels(channels):
    with open(DATA_FILE, "w") as f:
        json.dump(channels, f)

# --- Construir teclado ---
def build_keyboard():
    # Botón fijo (tu canal principal con el texto que pediste)
    keyboard = [[InlineKeyboardButton("ONLY FREE 🔥🔞", url="https://t.me/+SWJOLOSNQYVkM2Zk")]]
    
    # Botones de usuarios guardados
    channels = load_channels()
    for ch in channels:
        keyboard.append([InlineKeyboardButton(ch["name"], url=ch["url"])])
    return InlineKeyboardMarkup(keyboard)

# --- Comandos ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📢 Bienvenido!\n\nAquí puedes ver canales +18 promocionados o enviar el tuyo 👇",
        reply_markup=build_keyboard()
    )

# --- Cuando alguien envía un mensaje ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Verifica si es un link de Telegram
    if text.startswith("https://t.me/") or text.startswith("@"):
        channels = load_channels()

        # Evitar duplicados
        if any(ch["url"] == text for ch in channels):
            await update.message.reply_text("⚠️ Ese canal ya está en la lista.", reply_markup=build_keyboard())
            return

        # Guardar canal con nombre del usuario
        new_channel = {
            "name": f"Canal de {update.effective_user.first_name}",
            "url": text
        }
        channels.append(new_channel)
        save_channels(channels)

        await update.message.reply_text("✅ Tu canal fue añadido a la lista.", reply_markup=build_keyboard())
    else:
        await update.message.reply_text("❌ Solo acepto enlaces de canales de Telegram.")

# --- Función principal ---
def main():
    app = Application.builder().token(TOKEN).build()

    # Comando /start
    app.add_handler(CommandHandler("start", start))

    # Mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()