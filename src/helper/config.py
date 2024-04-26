import os, discord, random
from loguru import logger
from dotenv import load_dotenv

class Config:
    """
    Singleton class for managing configuration settings.

    Attributes:
        rainbow_line_gif (str): URL of the rainbow line GIF.
        app_logo (str): Logo of the application.
        app_url (str): URL of the application.
        app_name (str): Name of the application.
        app_name_branded (str): Branded name of the application.
        app_version (str): Version of the application.
        log_file (str): Path to the log file.
        proxies_file (str): Path to the file containing proxies.
        bot_prefix (str): Prefix for the Discord bot commands.
        bot_token (str): Token for the Discord bot.
        chat_category (int): ID of the Discord category for chat channels.
        dev_guild_id (discord.Object): ID of the development guild.
        additional_hide_roles (list): List of additional roles to hide chat channels from.

    Methods:
        reload(): Reloads the configuration from the YAML file.
        get_proxy(): Returns a random proxy from the list or None if proxyless.
        change_value(key, value): Changes the value of a configuration setting and saves it to the YAML file.

    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._load_env()
            self._load_config()
            self._update_attributes()
            self.proxies = self._load_proxies()
            self.proxyless = len(self.proxies) == 0

    def _load_env(self):
        """Loads environment variables from .env file."""
        load_dotenv()

    def _load_config(self):
        """Loads configuration from environment variables."""
        try:
            self.config = {
                "app_logo": os.getenv("APP_LOGO"),
                "app_url": os.getenv("APP_URL"),
                "app_name": os.getenv("APP_NAME"),
                "app_version": os.getenv("APP_VERSION"),
                "log_file": os.getenv("LOG_FILE"),
                "proxies_file": os.getenv("PROXIES_FILE"),
                "bot_prefix": os.getenv("BOT_PREFIX"),
                "bot_token": os.getenv("BOT_TOKEN"),
                "chat_category": os.getenv("CHAT_CATEGORY"),
                "dev_guild_id": os.getenv("DEV_GUILD_ID"),
                "additional_hide_roles": os.getenv("ADDITIONAL_HIDE_ROLES", "").split(","),
            }
        except Exception as e:
            logger.error(f"Error loading configuration from environment variables: {e}")
            self.config = {}

    def _update_attributes(self):
        """Updates instance attributes from the config dictionary."""
        # [STATIC]
        self.rainbow_line_gif: str = "https://i.imgur.com/mnydyND.gif"

        # [APP]
        self.app_logo: str = self.config.get("app_logo", "")
        self.app_url: str = self.config.get("app_url", "")
        self.app_name: str = self.config.get("app_name", "")
        self.app_name_branded: str = f"{self.app_name} • {self.app_url}"
        self.app_version: str = self.config.get("app_version", "")
        self.log_file: str = self.config.get("log_file", "")
        self.proxies_file: str = self.config.get("proxies_file", "")

        # [BOT]
        self.bot_prefix: str = self.config.get("bot_prefix", "")
        self.bot_token: str = self.config.get("bot_token", "")
        self.chat_category: int = int(self.config.get("chat_category", 0))
        self.dev_guild_id: discord.Object = discord.Object(int(self.config.get("dev_guild_id", 0)))
        self.additional_hide_roles: list = self.config.get("additional_hide_roles", [])

    def reload(self):
        """
        Reloads the configuration from the environment variables.

        Returns:
            bool: True if the configuration was successfully reloaded, False otherwise.
        """
        try:
            self._load_config()
            if self.config:
                self._update_attributes()
                self.proxies = self._load_proxies()
                self.proxyless = len(self.proxies) == 0
                logger.info("Successfully reloaded configuration from environment variables.")
                return True
            else:
                logger.warning("Failed to reload configuration.")
                return False
        except Exception as e:
            logger.critical(f"Failed to reload configuration: {e}")
            return False

    def _load_proxies(self):
        """
        Loads proxies from a file, returning a list or an empty list if file is not found or empty.

        Returns:
            list: List of proxies.
        """
        try:
            with open(self.proxies_file, 'r') as file:
                return [line.strip() for line in file if line.strip()]
        except FileNotFoundError:
            logger.warning(f"Proxy file {self.proxies_file} not found.")
            return []
        except Exception as e:
            logger.error(f"Error loading proxies: {e}")
            return []

    def get_proxy(self):
        """
        Returns a random proxy from the list or None if proxyless.

        Returns:
            str or None: Random proxy or None.
        """
        return random.choice(self.proxies) if self.proxies else None

    def change_value(self, key, value):
        """
        Changes the value of a configuration setting and saves it to the environment variables.

        Args:
            key (str): The key of the configuration setting.
            value: The new value of the configuration setting.

        Returns:
            bool: True if the value was successfully changed and saved, False otherwise.
        """
        try:
            os.environ[key] = str(value)
            logger.info(f"Changed value in environment variables: {key} -> {value}")
            return True
        except Exception as e:
            logger.critical(f"Failed to change value in environment variables: {e}")
            return False