import asyncio
from dataclasses import dataclass
from typing import Optional
from PIL import Image


@dataclass
class ProcessTask:
    text: str
    image: Optional[Image.Image] = None
    chat_id: Optional[int] = None
    message_id: Optional[int] = None

class Processor:
    def __init__(self, summarizer, send_result):
        self.queue: asyncio.Queue[ProcessTask] = asyncio.Queue()
        self._running = False
        self.summarizer = summarizer
        self.send_result = send_result

    async def enqueue(self, task: ProcessTask):
        await self.queue.put(task)

    async def _handle(self, task: ProcessTask):
        result = await self.summarizer.summarize(task.text, task.image)
        if task.chat_id and result:
            await self.send_result(task.chat_id, result, task.message_id)

    async def run(self):
        self._running = True
        while self._running:
            task = await self.queue.get()
            try:
                await self._handle(task)
            except Exception as e:
                print(f'Processor error: {e}')
            finally:
                self.queue.task_done()
