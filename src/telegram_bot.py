from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from dotenv import load_dotenv
load_dotenv()
import os
import io
from PIL import Image
from processor import Processor, ProcessTask
import asyncio

BOT_TOKEN = str(os.getenv('BOT_TOKEN'))
processor = Processor()

async def brief_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    processor: Processor = context.bot_data['processor']
    msg = update.message
    text = msg.text or msg.caption or ''
    image = None

    if msg.photo:
        photo = msg.photo[-1]
        file = await photo.get_file()

        image = Image.open(io.BytesIO(await file.download_as_bytearray()))
    print('echo')
    await processor.enqueue(ProcessTask(
        text=text,
        image=image,
        chat_id=msg.chat_id,
        message_id=msg.message_id
    ))
    
async def start(update: Update, context: ContextTypes):
    await update.message.reply_text('Bot working')

def build_app(processor: Processor):
    app = Application.builder().token(BOT_TOKEN).build()
    app.bot_data['processor'] = processor
    app.add_handler(MessageHandler(filters.FORWARDED, brief_post))
    app.add_handler(CommandHandler('start', start))
    return app