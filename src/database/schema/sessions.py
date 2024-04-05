class SessionSchema:
    def __init__(self, owner_id: int, discord_channel_id: int, last_used: str = None, ephemeral: bool = False) -> None:
        self.owner_id = owner_id
        self.discord_channel_id = discord_channel_id
        self.last_used = last_used
        self.ephemeral = ephemeral

    def serialize(self) -> dict:
        return {
            'owner_id': self.owner_id,
            'discord_channel_id': self.discord_channel_id,
            'last_used': self.last_used,
            'ephemeral': self.ephemeral
        }

    @staticmethod
    def deserialize(data_tuple):
        if not data_tuple:
            return None
        return SessionSchema(
            owner_id=data_tuple[1],
            discord_channel_id=data_tuple[2],
            last_used=data_tuple[3],
            ephemeral=bool(data_tuple[4])  # Convert to boolean
        )
