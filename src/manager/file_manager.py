import os
from loguru import logger
from src.helper.config import Config

# Default configuration template
DEFAULT_CONFIG = """
# [APP]
app_logo: 
app_name: 
app_url: 
app_version: 
log_file: 

# [BOT]
bot_prefix: 
bot_token: 
chat_category: 
dev_guild_id: 
logs_channel: 

# [AI]
api_endpoint: 
"""

class FileManager:
    """
    A class responsible for managing file and directory operations
    required for the application's configuration and data storage.
    """

    def __init__(self):
        """
        Initializes the FileManager and sets up a configuration object.
        """
        self.config = Config()

    def check_input(self):
        """
        Validates and sets up necessary files and directories.
        Creates a default configuration file if it does not exist.
        Ensures the presence of essential data and database directories.
        """
        # Check for config file and create if not found
        if not os.path.isfile("config.yaml"):
            logger.info("Config file not found. Creating a default configuration file...")
            with open("config.yaml", "w+") as config_file:
                config_file.write(DEFAULT_CONFIG)
            logger.info("A default config.yml has been created. Please configure it before proceeding.")
            return

        # Create the database directory
        self._create_directory("src/database")

        # Create the data directories
        self._create_directory("data/logs")
        self._create_directory("data/input")

    def _create_directory(self, path):
        """
        Creates a directory along with any necessary parent directories.

        Args:
            path (str): The directory path to create.
        """
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            logger.debug(f"{path} directory created.")