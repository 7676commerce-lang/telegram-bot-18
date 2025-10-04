import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import Update
from telegram.ext import CallbackContext

# 🔑 Pega tu token nuevo aquí entre comillas
TOKEN = "8298151817:AAFQCZCw2uGQOvDBI55sBpbQucFfzCWICew
"

canales_guardados = []

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "👋 Bienvenido al bot de promoción.\n\n"
        "📢 Envíame el enlace de tu canal y lo guardaré para que otros lo vean.\n"
        "👉 Usa /ver para ver la lista de canales."
    )

async def guardar_canal(update: Update, context: CallbackContext):
    link = update.message.text
    if link.startswith("https://t.me/"):
        canales_guardados.append(link)
        await update.message.reply_text("✅ Canal guardado con éxito.")
    else:
        await update.message.reply_text("❌ El enlace no es válido.")

async def ver(update: Update, context: CallbackContext):
    if canales_guardados:
        lista = "\n".join(canales_guardados)
        await update.message.reply_text(f"📢 Canales promocionados:\n\n{lista}")
    else:
        await update.message.reply_text("Aún no hay canales guardados.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ver", ver))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, guardar_canal))
    print("🤖 Bot en marcha...")
    app.run_polling()

if __name__ == "__main__":
    main()
