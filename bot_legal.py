import openai
import logging
import os
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# 🔹 Configuración con Variables de Entorno (para Railway)
TELEGRAM_BOT_TOKEN = os.getenv("8134572756:AAFVePIVX4KCxOPs0hQLaEDP-B3WfU0d4oQ")  # Token de BotFather
OPENAI_API_KEY = os.getenv("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
")  # API Key de OpenAI

# Inicializar OpenAI
openai.api_key = OPENAI_API_KEY

# Configurar logging
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# Función para responder mensajes con GPT-3.5
def responder(update: Update, context: CallbackContext):
    user_text = update.message.text
    logging.info(f"Consulta recibida: {user_text}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Eres un asistente experto en derecho penal boliviano. Responde con base en la ley."},
                      {"role": "user", "content": user_text}]
        )
        respuesta = response["choices"][0]["message"]["content"]
    except Exception as e:
        respuesta = "⚠️ Error al procesar la consulta."

    update.message.reply_text(respuesta)

# Iniciar el bot
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, responder))

    updater.start_polling()
    logging.info("🤖 Bot en ejecución...")
    updater.idle()

if __name__ == "__main__":
    main()
