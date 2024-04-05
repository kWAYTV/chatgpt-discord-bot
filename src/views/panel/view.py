import discord, uuid
from src.views.channel.control_view import ControlView
from src.database.schema.sessions import SessionSchema
from src.database.controller.sessions import SessionsController

class PanelView(discord.ui.View):
    def __init__(self):
        self.sessions = SessionsController()
        super().__init__(timeout=None)

    async def not_implemented(self, interaction: discord.Interaction):
        return await interaction.response.send_message("Sorry! This option is **not** yet implemented.", ephemeral=True)

    @discord.ui.button(label='➕ Create Room', style=discord.ButtonStyle.green, custom_id='panel:create_room')
    async def create_room_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Check if the user already has a session
        session = await self.sessions.get_session(interaction.user.id)
        if session is not None:
            return await interaction.response.send_message(f"You already have a room! You can access it at <#{session.discord_channel_id}>.", ephemeral=True)

        # Create a new private channel
        channel = await interaction.guild.create_text_channel(f"room-{uuid.uuid4()}", category=interaction.channel.category)
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(interaction.guild.me, read_messages=True, send_messages=True)

        # Add the session to the database
        new_session = SessionSchema(owner_id=interaction.user.id, discord_channel_id=channel.id)
        await self.sessions.create_session(new_session)

        # Tag the user in the new channel
        await channel.send(f"Hey {interaction.user.mention}! Welcome to your room!", view=ControlView())

        return await interaction.response.send_message(f"Your room has been created! You can access it at <#{channel.id}>.", ephemeral=True)

    @discord.ui.button(label='🗑️ Delete Rooms', style=discord.ButtonStyle.red, custom_id='panel:delete_room')
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
