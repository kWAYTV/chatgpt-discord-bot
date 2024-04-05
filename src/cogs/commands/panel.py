import discord, traceback
from loguru import logger
from discord.ext import commands
from discord import app_commands
from src.helper.config import Config
from src.views.panel.view import PanelView
from src.controller.discord.schema.embed_schema import EmbedSchema
from src.controller.discord.embed_controller import EmbedController

class Panel(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()

    @app_commands.command(name="panel", description="Send the bot interaction panel.")
    @app_commands.checks.has_permissions(administrator=True)
    async def panel_command(self, interaction: discord.Interaction, channel: discord.TextChannel = None, hidden: bool = False):
        try:

            if channel is None:
                channel = interaction.channel

            embed_schema = EmbedSchema(
                title="🤖 Welcome!",
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
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"You don't have the necessary permissions to use this command.",ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Panel(bot))
    logger.info("Panel command loaded!")