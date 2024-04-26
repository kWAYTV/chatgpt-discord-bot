import os
from loguru import logger
from src.helper.config import Config

# Default configuration template
DEFAULT_CONFIG = """
APP_LOGO=
APP_NAME=
APP_URL=
APP_VERSION=
LOG_FILE=
PROXIES_FILE=

BOT_PREFIX=
BOT_TOKEN=
CHAT_CATEGORY=
DEV_GUILD_ID=
ADDITIONAL_HIDE_ROLES=
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

    def check_input(self) -> bool:
        """
        Validates and sets up necessary files and directories.
        Creates a default configuration file if it does not exist.
        Ensures the presence of essential data and database directories.
        """
        # Check for config file and create if not found
        try:
            # Create the data directories
            self._create_directory("data/logs")
            self._create_directory("data/proxies")

            # Create the database directory
            self._create_directory("src/database")

            if not os.path.isfile(".env"):
                with open(".env", "w") as f:
                    f.write(DEFAULT_CONFIG)
                    logger.debug(".env configuration file created.")

            return True
        except Exception as e:
            logger.error(f"An error occurred while checking for file inputs: {e}")
            return False

    def _create_directory(self, path):
        """
        Creates a directory along with any necessary parent directories.

        Args:
            path (str): The directory path to create.
        """
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            logger.debug(f"{path} directory created.")