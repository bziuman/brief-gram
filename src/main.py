import asyncio
from telegram_bot import build_app
from processor import Processor
from summarizer import Summarizer

async def main():
    summarizer = await Summarizer.create()
    bot_ref = None

    async def send_result(chat_id, text, reply_to_message_id):
        await bot_ref.send_message(chat_id, text, reply_to_message_id=reply_to_message_id)

    processor = Processor(summarizer=summarizer, send_result=send_result)
    app = build_app(processor, summarizer)

    bot_ref = app.bot
    async with app:
        await app.start()
        await app.updater.start_polling()

        processor_task = asyncio.create_task(processor.run())

        try:
            await asyncio.Event().wait()
        except (KeyboardInterrupt, asyncio.CancelledError):
            pass
        finally:
            processor_task.cancel()
            await app.updater.stop()
            await app.stop()

if __name__ == '__main__':
    asyncio.run(main())