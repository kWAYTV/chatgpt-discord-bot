import discord
from loguru import logger
from discord.ext import commands
from discord import app_commands
from src.controller.discord.schema.embed_schema import EmbedSchema
from src.controller.discord.embed_controller import EmbedController
from src.database.schema.sessions import SessionSchema
from src.database.controller.sessions import SessionsController
from src.controller.ai.prompt_controller import PromptController

class Prompt(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.sessions = SessionsController()
        self.prompt_controller = PromptController.get_instance()

    @app_commands.command(name="prompt", description="Send a prompt to your room.")
    async def prompt_command(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=False)

            # Send the initial response message.
            message = await interaction.followup.send('Please wait for an answer from the model...')

            # Typing indicator context manager.
            async with interaction.channel.typing():
                response = await self.prompt_controller.send_prompt(self.user_prompt.value)

            # Handle the response accordingly.
            if response is None:
                return await message.edit(content='The model failed to respond. Please try again either now or later.')

            await message.edit(content=response)

            # Update the session with the last used timestamp.
            session_schema = SessionSchema(owner_id=interaction.user.id, discord_channel_id=interaction.channel.id)
            await self.sessions.update_session(session_schema)

        except Exception as e:
            logger.error(f'An error occurred while processing the prompt: {e}')
            await message.edit(content='An error occurred while processing your prompt request. Please try again later.')

    @prompt_command.error
    async def prompt_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"You don't have the necessary permissions to use this command.",ephemeral=True)
        else:
            await interaction.response.send_message(f"An error occurred with prompt command: {error}", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(Prompt(bot))
    logger.info("Prompt command loaded!")