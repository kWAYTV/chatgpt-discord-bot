import discord
from loguru import logger
from discord.ext import commands, tasks
from src.database.controller.sessions import SessionsController

class ExpiredSessionsLoop(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.del_exp_sessions.start()

    @tasks.loop(minutes=30)
    async def del_exp_sessions(self):
        logger.debug("Deleting expired sessions...")
        await SessionsController().delete_expired_sessions()

    @del_exp_sessions.before_loop
    async def before_del_exp_sessions(self) -> None:
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ExpiredSessionsLoop(bot))
    return logger.info("Expired Sessions loop loaded!")