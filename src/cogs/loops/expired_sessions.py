import discord
from loguru import logger
from discord.ext import commands, tasks
from src.database.controller.sessions import SessionsController

class ExpiredSessionsLoop(commands.Cog):
    """
    A Discord bot cog that handles expired sessions.

    This cog periodically checks for expired sessions, deletes the corresponding Discord channels,
    and notifies the users about their expired sessions.
    """

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.sessions_controller = SessionsController()
        self.del_exp_sessions.start()

    # Rest of the code...
class ExpiredSessionsLoop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.sessions_controller = SessionsController()
        self.del_exp_sessions.start()

    @tasks.loop(minutes=30)
    async def del_exp_sessions(self):
        try:
            expired_sessions = await self.sessions_controller.get_expired_sessions()
            await self.handle_expired_sessions(expired_sessions)
            await self.sessions_controller.delete_expired_sessions()
        except Exception as e:
            logger.error(f"Error processing expired sessions: {e}")

    async def handle_expired_sessions(self, sessions):
        for session in sessions:
            await self.delete_discord_channel(session.discord_channel_id)
            await self.notify_user(session.owner_id)

    async def delete_discord_channel(self, channel_id):
        channel = self.bot.get_channel(channel_id)
        if channel:
            try:
                await channel.delete()
            except discord.Forbidden:
                logger.error(f"Failed to delete channel {channel.id} for expired session.")
            except discord.HTTPException as e:
                logger.error(f"HTTP exception deleting channel {channel.id}: {e}")
        else:
            logger.error(f"Failed to find channel with ID {channel_id} to delete for expired session.")

    async def notify_user(self, user_id):
        user = self.bot.get_user(user_id)
        if user:
            try:
                await user.send("Your session has expired.")
            except discord.Forbidden:
                logger.error(f"Failed to DM user {user.id} about their expired session.")
            except discord.HTTPException as e:
                logger.error(f"HTTP exception DMing user {user.id}: {e}")
        else:
            logger.error(f"Failed to find user with ID {user_id} to DM about their expired session.")

    @del_exp_sessions.before_loop
    async def before_del_exp_sessions(self) -> None:
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExpiredSessionsLoop(bot))
    logger.debug("Expired Sessions loop loaded!")
