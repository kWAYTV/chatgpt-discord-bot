import traceback
from loguru import logger
from src.database.controller.sessions import SessionsController

class DatabaseLoader:
    """
    Class responsible for loading the database and setting it up.
    """

    def __init__(self) -> None:
        self.sessions_controller = SessionsController()

    async def setup(self) -> None:
        """
        Sets up the database by creating the necessary table.
        """
        try:
            await self.sessions_controller.create_table()
        except Exception as e:
            logger.critical(f"Error setting up database(s): {e}")
            traceback.print_exc()