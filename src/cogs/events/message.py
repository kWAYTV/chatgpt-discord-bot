import discord
from loguru import logger
from discord.ext import commands
from src.database.schema.sessions import SessionSchema
from src.database.controller.sessions import SessionsController
from src.controller.ai.prompt_controller import PromptController

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sessions_controller = SessionsController()
        self.prompt_controller = PromptController()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        # Ignore messages sent by the bot
        if message.author == self.bot.user:
            return

        session_channels = await self.sessions_controller.get_session_channels()

        if message.channel.id in session_channels:
            try:

                # Get the message author's session
                fetch_session = await self.sessions_controller.get_session(message.author.id)
                session_id = fetch_session.id if fetch_session is not None else None
                if session_id is None:
                    await message.channel.send('You do not have an active session. Please start a session first.')
                    return

                # Sending prompt to AI model
                response = await self.prompt_controller.send_prompt(session_id, message.content)
                if response is None:
                    await message.channel.send('The model failed to respond. Please try again either now or later.')
                    return

                # Sending AI model's response to the channel
                await message.channel.send(response)

                # Updating the session
                session_schema = SessionSchema(owner_id=message.author.id, discord_channel_id=message.channel.id)
                await self.sessions_controller.update_session(session_schema)

            except Exception as e:
                logger.error(f'An error occurred while processing the message: {e}')
                await message.channel.send('An error occurred while processing your message. Please try again later.')

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(OnMessage(bot))
    return logger.debug("On message event registered!")