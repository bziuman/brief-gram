from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
load_dotenv()
import os
import io
from PIL import Image

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    text = msg.text or msg.caption or ''

    if msg.photo:
        photo = msg.photo[-1]
        file = await photo.get_file()

        image = Image.open(io.BytesIO(await file.download_as_bytearray()))
        image.show()
    

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.FORWARDED, echo))
    app.run_polling()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Bot stopped')