import nest_asyncio
from loguru import logger
from g4f.client import Client
from src.helper.config import Config
from g4f.Provider import RetryProvider, __providers__, Phind, FreeChatgpt, Liaobots, You

class PromptController:
    _instance = None
    _my_providers = [Phind, FreeChatgpt, Liaobots, You]

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        if self._instance is not None:
            raise ValueError("An instance of PromptController already exists.")
        
        self.config = Config()
        # Get a random proxy from the config
        proxy = self.config.get_proxy()

        # Initialize the Client with the proxy
        self.client = Client(
            provider=RetryProvider(__providers__, shuffle=True),
            proxies=f"https://{proxy}"
        )
        nest_asyncio.apply()

    async def send_prompt(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f'An error occurred while sending a prompt to the model: {e}')
            return 'The model failed to respond. Please try again either now or later.'