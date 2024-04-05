import nest_asyncio
from g4f.client import Client
from g4f.Provider import RetryProvider, Phind, FreeChatgpt, Liaobots

from loguru import logger
from src.helper.config import Config


class PromptController:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise ValueError("An instance of PromptController already exists.")
        self.config = Config()
        self.client = Client(
            provider=RetryProvider([Phind, FreeChatgpt, Liaobots], shuffle=True),
        )
        nest_asyncio.apply()

    async def send_prompt(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content