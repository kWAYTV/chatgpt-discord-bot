import aiosqlite
from loguru import logger
from typing import List, Optional
from src.helper.config import Config
from src.database.schema.sessions import SessionSchema

class SessionsController:
    def __init__(self):
        self.config = Config()
        self.db_path = 'src/database/storage/sessions.sqlite'

    async def create_table(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS ssh_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    owner_id INTEGER NOT NULL,
                    discord_channel_id INTEGER NOT NULL,
                    last_used TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    ephemeral BOOLEAN NOT NULL DEFAULT FALSE
                );
            ''')
            await db.commit()

    async def create_session(self, session: SessionSchema) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('''
                    INSERT INTO ssh_sessions (owner_id, discord_channel_id, last_used, ephemeral)
                    VALUES (?, ?, CURRENT_TIMESTAMP, FALSE);
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
                    SET discord_channel_id = ?, last_used = CURRENT_TIMESTAMP, ephemeral = ?
                    WHERE owner_id = ?;
                ''', (session.discord_channel_id, session.ephemeral, session.owner_id))
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

    async def delete_expired_sessions(self) -> None:
        async with aiosqlite.connect(self.db_path) as db:
            try:
                await db.execute('DELETE FROM ssh_sessions WHERE last_used < datetime("now", "-30 minutes");')
                await db.commit()
            except Exception as e:
                logger.error(f"An error occurred while trying to delete expired sessions: {e}")
                await db.rollback()