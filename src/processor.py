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
    def __init__(self):
        self.queue: asyncio.Queue[ProcessTask] = asyncio.Queue()
        self._running = False

    async def enqueue(self, task: ProcessTask):
        await self.queue.put(task)

    async def _handle(self, task: ProcessTask):
        print('handle')
        print(f'task\n text: {task.text}\nimage: {task.image}\nchat id: {task.chat_id}\nmessage id: {task.message_id}')

    async def run(self):
        self._running = True
        while self._running:
            task = await self.queue.get()
            print(f'task:\n{task}')
            try:
                await self._handle(task)
            except Exception as e:
                print(f'Processor error: {e}')
            finally:
                self.queue.task_done()
