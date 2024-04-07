from loguru import logger
from g4f.client import AsyncClient as Client
from src.helper.config import Config
from g4f.Provider import RetryProvider, Phind, FreeChatgpt, Liaobots, You

class PromptController:
    _instance = None
    _my_providers = [Phind, FreeChatgpt, Liaobots, You]

    @classmethod
    def get_instance(cls):
        """Singleton pattern implementation to ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initializes the PromptController, sets up the GPT client with or without proxy."""
        if self._instance is not None:
            raise ValueError("An instance of PromptController already exists.")

        self.config = Config()
        proxy_url = self._get_proxy_url() if not self.config.proxyless else None

        # Initialize the GPT client with or without a proxy
        self.client = Client(
            provider=RetryProvider(self._my_providers, shuffle=False), 
            proxies=proxy_url
        )

    def _get_proxy_url(self) -> str:
        """Retrieves a proxy URL from the configuration, logs it, and returns the formatted proxy URL."""
        proxy = self.config.get_proxy()
        return f"http://{proxy}"

    async def send_prompt(self, prompt: str) -> str:
        """Sends a prompt to the GPT model and returns the response."""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                timeout=10
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f'Error in sending prompt: {e}')
            return 'The model failed to respond. Please try again later.'
