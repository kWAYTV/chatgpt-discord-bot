import discord
from loguru import logger
from datetime import datetime
from src.helper.config import Config
from src.controller.discord.schema.embed_schema import EmbedSchema

class EmbedController:
    """
    A class that handles the creation of Discord embeds.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.config = Config()

    async def build_embed(self, embed_schema: EmbedSchema) -> discord.Embed:
        try:
            embed = discord.Embed(
                title=embed_schema.title,
                description=embed_schema.description,
                color=embed_schema.color
            )

            for field in embed_schema.fields:
                embed.add_field(name=field['name'], value=field['value'], inline=field.get('inline', True))

            embed.set_author(name=self.config.app_name, icon_url=self.config.app_logo, url=self.config.app_url)
            embed.set_footer(text=embed_schema.footer_text or self.config.app_name, icon_url=self.config.app_logo)
            embed.set_thumbnail(url=embed_schema.thumbnail_url or self.config.app_logo)
            if embed_schema.image_url:
                embed.set_image(url=embed_schema.image_url)
            embed.timestamp = datetime.utcnow()

            return embed

        except Exception as e:
            logger.error(f"Failed to build embed: {e}")
            return discord.Embed(title="Error", description="Failed to build embed")
