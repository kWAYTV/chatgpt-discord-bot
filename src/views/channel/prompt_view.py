import discord
from loguru import logger
from src.helper.config import Config
from src.database.schema.sessions import SessionSchema
from src.database.controller.sessions import SessionsController
from src.controller.ai.prompt_controller import PromptController

class PromptModal(discord.ui.Modal, title='Send command to host'):
    def __init__(self):
        self.config = Config()
        self.sessions = SessionsController()
        self.prompt_controller = PromptController.get_instance()
        super().__init__()

    user_prompt = discord.ui.TextInput(label='Prompt', style=discord.TextStyle.long, placeholder='Enter the prompt you want to give to the model.')

    async def on_submit(self, interaction: discord.Interaction):
        session = await self.sessions.get_session(interaction.user.id)
        if session is None:
            return await interaction.response.send_message(f"You don't have any rooms!", ephemeral=True)
        
        await interaction.response.defer(ephemeral=session.ephemeral)

        # Send the initial response message.
        message = await interaction.followup.send('Please wait for an answer from the model...', ephemeral=True)

        # Typing indicator context manager.
        async with interaction.channel.typing():
            # Using PromptController in its context manager
            async with self.prompt_controller as controller:
                response = await controller.send_prompt(self.user_prompt.value)

        # Handle the response accordingly.
        if response is None:
            return await message.edit(content='The model failed to respond. Please try again either now or later.')

        await message.edit(content=f"*{self.user_prompt.value}*\n```{response}```")

        # Update the session with the last used timestamp.
        session_schema = SessionSchema(owner_id=interaction.user.id, discord_channel_id=interaction.channel.id)
        await self.sessions.update_session(session_schema)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        logger.error(f'An error occurred with a prompt modal: {error}')
        await interaction.response.send_message(f'Oops! Something went wrong: {error}', ephemeral=True)
