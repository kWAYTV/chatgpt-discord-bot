import discord, uuid
from loguru import logger
from src.helper.config import Config
from src.views.channel.control_view import ControlView
from src.database.schema.sessions import SessionSchema
from src.database.controller.sessions import SessionsController
from src.controller.discord.schema.embed_schema import EmbedSchema
from src.controller.discord.embed_controller import EmbedController

class PanelView(discord.ui.View):
    """
    Represents the panel view for the Discord bot.
    This view allows users to create and delete rooms.
    """

    def __init__(self):
        self.config = Config()
        self.sessions = SessionsController()
        super().__init__(timeout=None)

    async def not_implemented(self, interaction: discord.Interaction):
        return await interaction.response.send_message("Sorry! This option is **not** yet implemented.", ephemeral=True)

    @discord.ui.button(label='➕ Create New Room', style=discord.ButtonStyle.green, custom_id='panel:create_room')
    async def create_room_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        #try:
        # Check if the user already has a session
        session = await self.sessions.get_session(interaction.user.id)
        if session is not None:
            return await interaction.response.send_message(f"You already have a room! You can access it at <#{session.discord_channel_id}>.", ephemeral=True)

        chat_category = interaction.guild.get_channel(self.config.chat_category) or interaction.channel.category

        # Create a new private channel
        channel = await interaction.guild.create_text_channel(f"room-{uuid.uuid4()}", category=chat_category)

        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(interaction.guild.me, read_messages=True, send_messages=True)
        await channel.set_permissions(interaction.guild.default_role, read_messages=False)

        # Hide additional roles if specified in the config
        for role_id in self.config.additional_hide_roles:
            role = interaction.guild.get_role(role_id)
            if not role: 
                return logger.warning(f"Role ID {role_id} not found in guild.")
            else: await channel.set_permissions(role, read_messages=False)

        # Add the session to the database
        new_session = SessionSchema(owner_id=interaction.user.id, discord_channel_id=channel.id)
        await self.sessions.create_session(new_session)

        # Tag the user in the new channel
        embed_schema = EmbedSchema(
            description="*Keep in mind the bot's using a reversed API and it might fail sometimes, if that's the case, retry or try later.*", 
            color=0x00ff00
        )
        embed = await EmbedController().build_embed(embed_schema)

        # Send the embed with the control view and notify the user in the panel channel to switch to the new channel
        await channel.send(content=f"Hey {interaction.user.mention}! Welcome to your room!", embed=embed, view=ControlView())
        return await interaction.response.send_message(f"Your room has been created! You can access it at <#{channel.id}>.", ephemeral=True)

        """ except Exception as e:
            logger.error(f"Failed to create a new room: {e}")
            return await interaction.response.send_message(f"Failed to create your room, if you don't see any, press the delete my rooms button and try again.", ephemeral=True) """

    @discord.ui.button(label='🗑️ Delete My Rooms', style=discord.ButtonStyle.red, custom_id='panel:delete_room')
    async def delete_room_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if the user has a session
        session = await self.sessions.get_session(interaction.user.id)
        if session is None:
            return await interaction.response.send_message("You don't have any rooms!", ephemeral=True)

        # Delete the private channel
        channel = interaction.guild.get_channel(session.discord_channel_id)
        if channel is not None:
            try:
                await channel.delete()
            except discord.errors.NotFound:
                pass  # Channel is already deleted or not found
            except Exception as e:
                return await interaction.response.send_message(f"Failed to delete your room: {e}", ephemeral=True)

        # Remove the session from the database
        await self.sessions.delete_session(interaction.user.id)

        return await interaction.response.send_message("Your rooms have been deleted!", ephemeral=True)
