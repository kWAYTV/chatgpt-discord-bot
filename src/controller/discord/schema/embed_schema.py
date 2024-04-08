# EmbedSchema.py
class EmbedSchema:
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
