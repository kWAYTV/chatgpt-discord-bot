# Imports
import os, discord, time
from loguru import logger
from traceback import format_exc
from discord.ext import commands
from src.helper.config import Config
from src.database.loader import DatabaseLoader
from src.manager.file_manager import FileManager

# Set logging system handler
logger.add(Config().log_file, mode="w+")

# Define the bot & load the commands, events and loops
class Bot(commands.Bot):
    def __init__(self) -> None:
        """
        Initializes the Bot class.

        Args:
            None

        Returns:
            None
        """
        super().__init__(
            command_prefix=Config().bot_prefix, 
            help_command=None, 
            intents=discord.Intents.all()
        )
        self.start_time = time.time()

    async def setup_hook(self) -> None:
        """
        Loads the necessary extensions, sets up the database, and initializes the bot.

        Args:
            None

        Returns:
            None
        """
        try:
            os.system("cls||clear")
            logger.info("Setting up bot...")

            # Check for file inputs
            logger.debug("Checking for file inputs...")
            FileManager().check_input()

            # Set-up the database
            logger.debug("Setting up databases...")
            await DatabaseLoader().setup()

            # Load the cogs
            logger.debug("Loading cogs...")
            for filename in os.listdir("./src/cogs/commands"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.commands.{filename[:-3]}")

            # Load the events
            logger.debug("Loading events...")
            for filename in os.listdir("./src/cogs/events"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.events.{filename[:-3]}")

            # Load the loops
            logger.debug("Loading loops...")
            for filename in os.listdir("./src/cogs/loops"):
                if filename.endswith(".py") and not filename.startswith("_"):
                    await self.load_extension(f"src.cogs.loops.{filename[:-3]}")

            # Done!
            logger.info("Setup completed!")
        except Exception:
            logger.critical(f"Error setting up bot: {format_exc()}")
            exit()

    async def close(self) -> None:
        """
        Shuts down the bot.

        Args:
            None

        Returns:
            None
        """
        await super().close()

# Run the bot
if __name__ == "__main__":
    try:
        bot = Bot()
        bot.run(Config().bot_token)
    except KeyboardInterrupt:
        logger.critical("Goodbye!")
        exit()
    except Exception:
        logger.critical(f"Error running bot: {format_exc()}")
        exit()
