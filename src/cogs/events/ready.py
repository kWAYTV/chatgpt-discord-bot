import os
from time import time
from loguru import logger
from pyfiglet import Figlet
from discord.ext import commands
from src.helper.config import Config
from src.views.panel.view import PanelView
from pystyle import Colors, Colorate, Center
from src.views.channel.control_view import ControlView

class OnReady(commands.Cog):
    """
    A Discord cog that handles the on_ready event.

    Attributes:
        bot (discord.ext.commands.Bot): The bot instance.
        config (Config): The configuration object.
    """

    def __init__(self, bot):
        self.bot = bot
        self.config = Config()

    @commands.Cog.listener()
    async def on_ready(self):
        """
        A coroutine that is called when the bot is ready.

        It clears the console, prints a logo, sets persistent views, and logs the login information.
        """

        os.system("cls||clear")

        logo = Figlet(font="big").renderText(self.config.app_name)
        centered_logo = Center.XCenter(Colorate.Vertical(Colors.white_to_blue, logo, 1))
        divider = Center.XCenter(Colorate.Vertical(Colors.white_to_blue, "────────────────────────────────────────────", 1))
        print(f"{centered_logo}\n{divider}\n\n")

        # Make the views persistent
        logger.debug("Setting persistent views...")
        self.bot.add_view(PanelView())
        self.bot.add_view(ControlView())
        
        elapsed_time = time() - self.bot.start_time
        logger.info(f"Logged in as {self.bot.user.name}#{self.bot.user.discriminator} ({elapsed_time:.2f}s)")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnReady(bot))
    return logger.debug("On ready event registered!")