from loguru import logger
from src.helper.config import Config
from g4f.client import AsyncClient as Client
from src.database.controller.sessions import SessionsController
from g4f.Provider import RetryProvider, Phind, FreeChatgpt, Liaobots, You

class PromptController:
    _instance = None
    _my_providers = [Phind, FreeChatgpt, Liaobots, You]

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initializes the PromptController, sets up the GPT client with or without proxy."""
        if not self._initialized:
            self.config = Config()
            self.sessions_controller = SessionsController()

            # Initialize the GPT client with or without a proxy
            proxy_url = self._get_proxy_url() if not self.config.proxyless else None
            self.client = Client(
                provider=RetryProvider(self._my_providers, shuffle=False), 
                proxies=proxy_url
            )

    def _get_proxy_url(self) -> str:
        """Retrieves a proxy URL from the configuration, logs it, and returns the formatted proxy URL."""
        proxy = self.config.get_proxy()
        return f"http://{proxy}"

    def _rotate_proxy(self):
        """Rotates the proxy used by the GPT client."""
        proxy_url = self._get_proxy_url()
        self.client.proxies = proxy_url

    async def send_prompt(self, session_id: int, user_input: str) -> str:
        """Sends a prompt to the GPT model and saves the interaction in the database."""
        try:
            # Save user input to chat history
            await self.sessions_controller.add_message(session_id, "user", user_input)

            # Retrieve chat history for the session
            chat_history = await self.sessions_controller.get_chat_history(session_id)

            # Send the updated chat history to the GPT model
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=chat_history,
                timeout=10
            )
            response_content = response.choices[0].message.content

            # Save model's response to chat history
            await self.sessions_controller.add_message(session_id, "assistant", response_content)
            return response_content

        except Exception as e:
            self._rotate_proxy()
            logger.error(f'Error in sending prompt: {e}')
            return 'The model failed to respond. Please try again later.'
