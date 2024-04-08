import aiosqlite, gzip, base64
from loguru import logger
from typing import List, Optional
from src.helper.config import Config
from src.database.schema.sessions import SessionSchema

class SessionsController:
    """
    Controller class for managing sessions in the database.
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
            self.db_path = 'src/database/storage/sessions.sqlite'

    async def create_table(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS ssh_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER NOT NULL,
                    discord_channel_id INTEGER NOT NULL,
                    last_used TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            await db.execute('''
                CREATE TABLE IF NOT EXISTS chat_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    message_role TEXT,
                    message_content TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES ssh_sessions(id)
                );
            ''')
            await db.commit()

    async def create_session(self, session: SessionSchema) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO ssh_sessions (owner_id, discord_channel_id, last_used)
                    VALUES (?, ?, CURRENT_TIMESTAMP);
                ''', (session.owner_id, session.discord_channel_id))
                await db.commit()
            except Exception as e:
                logger.error(f"An error occurred while trying to create session: {e}")
                await db.rollback()

    async def delete_session(self, owner_id: int) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('DELETE FROM ssh_sessions WHERE owner_id = ?;', (owner_id,))
                await db.commit()
            except Exception as e:
                logger.error(f"An error occurred while trying to delete session: {e}")
                await db.rollback()

    async def update_session(self, session: SessionSchema) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    UPDATE ssh_sessions
                    SET discord_channel_id = ?, last_used = CURRENT_TIMESTAMP
                    WHERE owner_id = ?;
                ''', (session.discord_channel_id, session.owner_id))
                await db.commit()
            except Exception as e:
                logger.error(f"An error occurred while trying to update session: {e}")
                await db.rollback()

    async def get_session(self, owner_id: int) -> Optional[SessionSchema]:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute('''
                    SELECT * FROM ssh_sessions WHERE owner_id = ?;
                ''', (owner_id,))
                row = await cursor.fetchone()
                if row is None:
                    return None
                return SessionSchema.deserialize(row)
            except Exception as e:
                logger.error(f"An error occurred while trying to get session: {e}")
                return None

    async def get_all_sessions(self) -> List[SessionSchema]:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute('SELECT * FROM ssh_sessions;')
                rows = await cursor.fetchall()
                return [SessionSchema.deserialize(row) for row in rows]
            except Exception as e:
                logger.error(f"An error occurred while trying to get all sessions: {e}")
                return []

    async def get_recent_sessions(self) -> List[SessionSchema]:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute('''
                    SELECT * FROM ssh_sessions WHERE last_used > datetime('now', '-1 day');
                ''')
                rows = await cursor.fetchall()
                return [SessionSchema.deserialize(row) for row in rows]
            except Exception as e:
                logger.error(f"An error occurred while trying to get recent sessions: {e}")
                return []

    async def get_session_channels(self) -> List[int]:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute('SELECT discord_channel_id FROM ssh_sessions;')
                rows = await cursor.fetchall()
                return [row[0] for row in rows]
            except Exception as e:
                logger.error(f"An error occurred while trying to get session channels: {e}")
                return []

    async def get_expired_sessions(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute('''
                    SELECT * FROM ssh_sessions WHERE last_used < datetime('now', '-30 minutes');
                ''')
                rows = await cursor.fetchall()
                return [SessionSchema.deserialize(row) for row in rows]
            except Exception as e:
                logger.error(f"An error occurred while trying to get expired sessions: {e}")
                return []

    async def delete_expired_sessions(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    DELETE FROM ssh_sessions WHERE last_used < datetime('now', '-30 minutes');
                ''')
                await db.commit()
            except Exception as e:
                logger.error(f"An error occurred while trying to delete expired sessions: {e}")
                await db.rollback()

    async def add_message(self, session_id: int, message_role: str, message_content: str) -> None:
        compressed_content = self._compress_message(message_content)
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO chat_messages (session_id, message_role, message_content)
                    VALUES (?, ?, ?);
                ''', (session_id, message_role, compressed_content))
                await db.commit()
            except Exception as e:
                logger.error(f"Error adding message: {e}")
                await db.rollback()

    async def get_chat_history(self, session_id: int) -> List[dict]:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                cursor = await db.execute('''
                    SELECT message_role, message_content FROM chat_messages
                    WHERE session_id = ? ORDER BY timestamp;
                ''', (session_id,))
                rows = await cursor.fetchall()
                return [{"role": row[0], "content": self._decompress_message(row[1])} for row in rows]
            except Exception as e:
                logger.error(f"Error retrieving chat history: {e}")
                return []

    def _compress_message(self, message: str) -> str:
        return base64.b64encode(gzip.compress(message.encode())).decode()

    def _decompress_message(self, compressed_message: str) -> str:
        return gzip.decompress(base64.b64decode(compressed_message)).decode()