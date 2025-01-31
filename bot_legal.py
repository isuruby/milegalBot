import os
import logging
from openai import OpenAI
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackContext

# 🔹 Cargar las variables de entorno desde .env
load_dotenv()

# 🔹 Obtener claves desde el sistema o el archivo .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

# 🔹 Verificar si las claves se están cargando correctamente
print(f"🔹 Token de Telegram cargado: '{TELEGRAM_BOT_TOKEN}' (Longitud: {len(TELEGRAM_BOT_TOKEN)})")
print(f"🔹 Clave de OpenAI cargada: (Longitud: {len(OPENAI_API_KEY)})")

# 🔹 Validar que las claves existen antes de continuar
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ ERROR: El token de Telegram no está configurado o es incorrecto.")

if not OPENAI_API_KEY:
    raise ValueError("❌ ERROR: La clave API de OpenAI no está configurada o es incorrecta.")

# 🔹 Inicializar OpenAI con la nueva API
client = OpenAI(api_key=OPENAI_API_KEY)

# 🔹 Configurar logging para depuración en Railway
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO)

# 🔹 Función para responder mensajes con OpenAI
async def responder(update: Update, context: CallbackContext):
    user_text = update.message.text
    logging.info(f"Consulta recibida: {user_text}")

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un asistente experto en derecho penal boliviano. Responde con base en la ley."},
                {"role": "user", "content": user_text}
            ]
        )
        respuesta = response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error con OpenAI: {e}")
        respuesta = "⚠️ Error al procesar la consulta."

    await update.message.reply_text(respuesta)

# 🔹 Iniciar el bot
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    logging.info("🤖 Bot en ejecución...")
    app.run_polling()

if __name__ == "__main__":
    main()
