class SessionSchema:
    def __init__(self, owner_id: int, discord_channel_id: int, last_used: str = None, id: int = None) -> None:
        """
        Initialize a SessionSchema object.

        Args:
            owner_id (int): The ID of the owner of the session.
            discord_channel_id (int): The ID of the Discord channel associated with the session.
            last_used (str, optional): The last time the session was used. Defaults to None.
            id (int, optional): The ID of the session. Defaults to None.
        """
        self.id = id
        self.owner_id = owner_id
        self.discord_channel_id = discord_channel_id
        self.last_used = last_used

    def serialize(self) -> dict:
        """
        Serialize the SessionSchema object into a dictionary.

        Returns:
            dict: The serialized session data.
        """
        return {
            'id': self.id,
            'owner_id': self.owner_id,
            'discord_channel_id': self.discord_channel_id,
            'last_used': self.last_used,
        }

    @staticmethod
    def deserialize(data_tuple):
        """
        Deserialize the session data from a tuple.

        Args:
            data_tuple: The tuple containing the session data.

        Returns:
            SessionSchema: The deserialized SessionSchema object.
        """
        if not data_tuple:
            return None
        return SessionSchema(
            id=data_tuple[0],
            owner_id=data_tuple[1],
            discord_channel_id=data_tuple[2],
            last_used=data_tuple[3],
        )