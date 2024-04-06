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
        self.prompt_controller = PromptController.get_instance()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        # Ignore messages sent by the bot
        if message.author == self.bot.user:
            return

        session_channels = await self.sessions_controller.get_session_channels()

        if message.channel.id in session_channels:
            logger.info(f"Message sent in session channel: {message.content}({message.channel.id})")
            try:
                # Sending prompt to AI model
                response = await self.prompt_controller.send_prompt(message.content)
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
    return logger.info("On message event registered!")