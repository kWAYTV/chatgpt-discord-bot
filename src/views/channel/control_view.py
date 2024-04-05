import discord
from loguru import logger
from src.views.channel.prompt_view import PromptModal
from src.database.controller.sessions import SessionsController

class ControlView(discord.ui.View):
    def __init__(self):
        self.sessions = SessionsController()
        super().__init__(timeout=None)

    async def not_implemented(self, interaction: discord.Interaction):
        return await interaction.response.send_message("Sorry! This option is **not** yet implemented.", ephemeral=True)

    @discord.ui.button(label='💬 Prompt', style=discord.ButtonStyle.green, custom_id='control:prompt')
    async def prompt_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        return await interaction.response.send_modal(PromptModal())

    @discord.ui.button(label='👁️ Hidden Messages', style=discord.ButtonStyle.blurple, custom_id='control:ephemeral_room')
    async def ephemeral_room_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        session = await self.sessions.get_session(interaction.user.id)
        if session is None:
            return await interaction.response.send_message(f"You don't have any rooms!", ephemeral=True)

        try:
            session.ephemeral = not session.ephemeral
            await self.sessions.update_session(session)
            return await interaction.response.send_message(f"Room messages are now {'hidden' if session.ephemeral else 'visible'}!", ephemeral=True)
        except Exception as e:
            logger.error(f"An error occurred while trying to update the session ephemeral mode: {e}")
            return await interaction.response.send_message(f"An error occurred while trying to update the session message visibility.", ephemeral=True)

    @discord.ui.button(label='🗑️ Delete Room', style=discord.ButtonStyle.red, custom_id='control:delete_room')
    async def delete_room_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        session = await self.sessions.get_session(interaction.user.id)
        if session is None:
            return await interaction.response.send_message(f"You don't have any rooms!", ephemeral=True)

        # Delete the private channel
        try:
            channel = interaction.guild.get_channel(interaction.channel.id)

            await channel.delete()
            await self.sessions.delete_session(interaction.user.id)
        except Exception as e:
            logger.error(f"An error occurred while trying to delete the room: {e}")
            return await interaction.response.send_message(f"An error occurred while trying to delete the room: {e}", ephemeral=True)