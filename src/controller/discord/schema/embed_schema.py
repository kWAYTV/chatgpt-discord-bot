# EmbedSchema.py
class EmbedSchema:
    """
    Represents an embed schema for Discord messages.

    Args:
        title (str): The title of the embed.
        description (str): The description of the embed.
        fields (list): A list of fields in the embed.
        color (int): The color of the embed.
        thumbnail_url (str): The URL of the thumbnail image.
        image_url (str): The URL of the main image.
        footer_text (str): The text in the footer of the embed.
        author_url (str): The URL of the author's profile.

    Attributes:
        title (str): The title of the embed.
        description (str): The description of the embed.
        fields (list): A list of fields in the embed.
        color (int): The color of the embed.
        thumbnail_url (str): The URL of the thumbnail image.
        image_url (str): The URL of the main image.
        footer_text (str): The text in the footer of the embed.
        author_url (str): The URL of the author's profile.
    """

    def __init__(self, title=None, description=None, fields=None, color=0xb34760,
                    thumbnail_url=None, image_url=None, footer_text=None, author_url=None):
        self.title = title
        self.description = description
        self.fields = fields if fields is not None else []
        self.color = color
        self.thumbnail_url = thumbnail_url
        self.image_url = image_url
        self.footer_text = footer_text
        self.author_url = author_url

    def __repr__(self):
        return (f"<EmbedSchema title={self.title} description={self.description} "
                f"fields={self.fields} color={self.color} thumbnail_url={self.thumbnail_url} "
                f"image_url={self.image_url} footer_text={self.footer_text}>")
