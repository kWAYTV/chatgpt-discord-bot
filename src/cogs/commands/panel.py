import discord, traceback
from loguru import logger
from discord.ext import commands
from discord import app_commands
from src.helper.config import Config
from src.views.panel.view import PanelView
from src.controller.discord.schema.embed_schema import EmbedSchema
from src.controller.discord.embed_controller import EmbedController

class Panel(commands.Cog):
    """
    A Discord bot command cog for managing the bot interaction panel.

    This cog provides a command to send the bot interaction panel to a specified channel or the current interaction channel.
    The panel includes options for managing the bot.

    Attributes:
        bot (commands.Bot): The instance of the Discord bot.
        config (Config): The configuration object for the bot.

    Methods:
        panel_command: The command function for sending the bot interaction panel.
        panel_command_error: The error handler for the panel command.

    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()

    @app_commands.command(name="panel", description="Send the bot interaction panel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def panel_command(self, interaction: discord.Interaction, channel: discord.TextChannel = None, hidden: bool = False):
        """
        Send the bot interaction panel.

        This command sends the bot interaction panel to the specified channel or the current interaction channel.
        The panel includes options for managing the bot.

        Parameters:
            interaction (discord.Interaction): The Discord interaction object.
            channel (discord.TextChannel, optional): The channel to send the panel to. Defaults to None.
            hidden (bool, optional): Whether the panel should be hidden. Defaults to False.

        Raises:
            app_commands.errors.MissingPermissions: If the user does not have the necessary permissions.

        """
        try:

            if channel is None:
                channel = interaction.channel

            embed_schema = EmbedSchema(
                description=f"From this panel you will be able to manage the bot.",
                color=0xb34760
            )

            embed = await EmbedController().build_embed(embed_schema)
            await channel.send(embed=embed, view=PanelView())
            await interaction.response.send_message(f"Panel sent in {channel.mention}({channel.id})!", ephemeral=True)

        except Exception:
            await interaction.followup.send(f"An error occurred with panel command: {traceback.print_exc}", ephemeral=True)
            logger.critical(f"An error occurred with panel command: {traceback.print_exc}")

    @panel_command.error
    async def panel_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """
        Handle errors for the panel command.

        This method is called when an error occurs in the panel command.
        It sends an error message to the user based on the type of error.

        Parameters:
            interaction (discord.Interaction): The Discord interaction object.
            error (app_commands.AppCommandError): The error that occurred.

        """
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"You don't have the necessary permissions to use this command.",ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Panel(bot))
    logger.debug("Panel command loaded!")