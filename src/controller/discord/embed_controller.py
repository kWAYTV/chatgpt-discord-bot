import discord
from loguru import logger
from datetime import datetime
from src.helper.config import Config
from src.controller.discord.schema.embed_schema import EmbedSchema

class EmbedController:
    """
    A class that handles the creation of Discord embeds.
    """

    def __init__(self):
        self.config = Config()
    
    async def build_embed(self, embed_schema: EmbedSchema) -> discord.Embed:
        """
        Builds a Discord embed based on the provided embed schema.
        """
        try:
            schema = embed_schema.get_schema()
            embed = discord.Embed(
                title=schema["title"],
                description=schema["description"],
                color=schema["color"]
            )

            # Add fields to embed
            if schema.get("fields") is not None:
                for field in schema.get("fields", []):
                    if field.get("value") is not None:
                        embed.add_field(
                            name=field["name"],
                            value=field["value"],
                            inline=field.get("inline", False)
                        )

            # Set default properties
            self.set_defaults(embed, schema)

            # Set timestamp
            embed.timestamp = datetime.utcnow()
            return embed

        except Exception as e:
            logger.error(f"Failed to build embed: {e}")
            return discord.Embed(title="Error", description="Failed to build embed")

    def set_defaults(self, embed: discord.Embed, schema: dict):
        """
        Sets default values for various properties of the embed.
        """
        author_name = schema.get('author_name', self.config.app_name)
        author_icon_url = schema.get('author_icon_url', self.config.app_logo)
        author_url = schema.get('author_url', self.config.app_url)
        footer_text = schema.get('footer_text', self.config.app_name)
        footer_icon_url = schema.get('footer_icon_url', self.config.app_logo)
        image_url = schema.get('image_url', '')
        thumbnail_url = schema.get('thumbnail_url', self.config.app_logo)

        embed.set_author(name=author_name, icon_url=author_icon_url, url=author_url)
        embed.set_footer(text=footer_text, icon_url=footer_icon_url)
        embed.set_thumbnail(url=thumbnail_url)
        embed.set_image(url=image_url)
