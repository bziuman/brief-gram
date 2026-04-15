import ollama
import asyncio

class Summarizer:
    def __init__(self):
      self.models_list = []
      self.active_llm_model = ''
      self.promtp = '''
                        Ты аналітик.
                        Дай:
                        1. Короткий переказ (2-3 речення)
                        2. Суть (1 речення)
                        3. В чому використовувати (список)

                        Текст:
                        {text}
                    '''

    @classmethod
    async def create(cls):
        self = cls()
        await self._init_models()
        return self
    
    async def _init_models(self):
        self.models_list = await self.get_model_list()
        self.active_llm_model = self.models_list[0]

    async def get_model_list(self):
        request = await asyncio.to_thread(ollama.list) 
        self.models_list = []
        for model in request['models']:
            self.models_list.append(model['model'])
        return self.models_list
    
    async def change_llm_model(self, id):
        self.active_llm_model = self.models_list[id]

    async def summarize(self, text, image):
        prompt = self.promtp.format(text=text)
        print(prompt)
        response = await asyncio.to_thread(ollama.chat,
            model=self.active_llm_model,
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )
        return response['message']['content']

    async def set_prompt(self, text):
        self.promtp = text