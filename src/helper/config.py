import discord, yaml, random
from loguru import logger
from yaml import SafeLoader, YAMLError

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._initialized = True
            self._load_config()
            self._update_attributes()
            self.proxies = self._load_proxies()
            self.proxyless = len(self.proxies) == 0

    def _load_config(self):
        """Loads configuration from the YAML file."""
        try:
            with open("config.yaml", "r") as file:
                self.config = yaml.load(file, Loader=SafeLoader)
        except FileNotFoundError:
            logger.error("Config file not found.")
            self.config = {}
        except YAMLError as e:
            logger.error(f"Error parsing config file: {e}")
            self.config = {}

    def _update_attributes(self):
        """Updates instance attributes from the config dictionary."""

        # [STATIC]
        self.rainbow_line_gif: str = "https://i.imgur.com/mnydyND.gif"

        # [APP]
        self.app_logo: str = self.config["app_logo"]
        self.app_url: str = self.config["app_url"]
        self.app_name: str = self.config["app_name"]
        self.app_name_branded: str = f"{self.app_name} • {self.app_url}"
        self.app_version: str = self.config["app_version"]
        self.log_file: str = self.config["log_file"]
        self.proxies_file: str = self.config["proxies_file"]

        # [BOT]
        self.bot_prefix: str = self.config["bot_prefix"]
        self.bot_token: str = self.config["bot_token"]
        self.chat_category: int = int(self.config["chat_category"])
        self.dev_guild_id: discord.Object = discord.Object(int(self.config["dev_guild_id"]))
        self.additional_hide_roles: list = self.config["additional_hide_roles"]

    def reload(self):
        try:
            self._load_config()
            if self.config:
                self._update_attributes()
                self.proxies = self._load_proxies()
                self.proxyless = len(self.proxies) == 0
                logger.info("Successfully reloaded config.yaml file.")
                return True
            else:
                logger.warning("Failed to reload the config file.")
                return False
        except Exception as e:
            logger.critical(f"Failed to reload config.yaml: {e}")
            return False

    def _load_proxies(self):
        """Loads proxies from a file, returning a list or an empty list if file is not found or empty."""
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
        """Returns a random proxy from the list or None if proxyless."""
        return random.choice(self.proxies) if self.proxies else None

    def change_value(self, key, value):
        try:
            config = self._load_config()
            config[key] = value
            with open("config.yaml", "w") as file:
                yaml.dump(config, file)
            self._update_attributes() # Update in-memory config to reflect changes
            logger.info(f"Changed value in config.yaml: {key} -> {value}, the file was rewritten.")
            return True
        except Exception as e:
            logger.critical(f"Failed to change value in config.yaml: {e}")
            return False
