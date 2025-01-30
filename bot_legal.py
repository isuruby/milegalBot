import os
import openai
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext

# 🔹 Obtener claves desde las variables de entorno (Railway)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()  # Elimina espacios extra
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()  # Elimina espacios extra

# 🔹 Validar que las claves existen antes de continuar
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ ERROR: El token de Telegram no está configurado en las variables de entorno.")

if not OPENAI_API_KEY:
    raise ValueError("❌ ERROR: La clave API de OpenAI no está configurada en las variables de entorno.")

# 🔹 Configurar OpenAI
openai.api_key = OPENAI_API_KEY

# 🔹 Configurar logging para ver mensajes en Railway
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🔹 Función para responder mensajes con GPT-3.5
async def responder(update: Update, context: CallbackContext):
    user_text = update.message.text
    logging.info(f"Consulta recibida: {user_text}")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en derecho penal boliviano. Responde con base en la ley."},
                {"role": "user", "content": user_text}
            ]
        )
        respuesta = response["choices"][0]["message"]["content"]
    except Exception as e:
        logging.error(f"Error con OpenAI: {e}")
        respuesta = "⚠️ Error al procesar la consulta."

    await update.message.reply_text(respuesta)

# 🔹 Iniciar el bot usando `ApplicationBuilder`
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Manejar solo mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    logging.info("🤖 Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()
