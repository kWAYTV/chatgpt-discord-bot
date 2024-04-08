import discord
from loguru import logger
from discord.ext import commands
from src.helper.config import Config

class SyncCommand(commands.Cog):
    """
    A Discord bot command cog for syncing slash commands.

    Attributes:
        bot (commands.Bot): The Discord bot instance.
        config (Config): The configuration object.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config = Config()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def sync(self, ctx: commands.Context, guild: discord.Guild = None):
        """
        Syncs slash commands globally or for a specific guild.

        Args:
            ctx (commands.Context): The command context.
            guild (discord.Guild, optional): The guild to sync slash commands for. Defaults to None.
        """
        try:
            await ctx.message.delete()
        except:
            logger.warning("Tried to delete a message that was not found.")
            pass

        try:
            if guild is None:
                await self.bot.tree.sync()
                success_message = "✅ Successfully synced slash commands globally!"
            else:
                await self.bot.tree.sync(guild=guild)
                success_message = f"✅ Successfully synced slash commands in {guild.name}!"
            msg = await ctx.send(success_message)
            
            logger.info("Slash commands were synced by an admin.")

            # Delete the success message after a delay
            await msg.delete(delay=5)

        except Exception as e:
            error_message = f"❌ Failed to sync slash commands: {e}"
            await ctx.send(error_message, delete_after=10)  # Optionally delete the error message after a delay
            logger.critical(error_message)

async def setup(bot: commands.Bot):
    await bot.add_cog(SyncCommand(bot))
    logger.debug("Sync command loaded!")