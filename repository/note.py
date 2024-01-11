from sqlalchemy.sql import select
from sqlalchemy import update, delete as sql_delete

from config import db

from models.note import Note


class NoteRepository:
    @staticmethod
    async def create(note_data: Note):
        async with db as session:
            async with session.begin():
                session.add(note_data)
            await db.commit_rollback()

    @staticmethod
    async def get_by_id(note_id: int) -> Note:
        async with db as session:
            stmt = select(Note).where(Note.id == note_id)
            result = await session.execute(stmt)
            note = result.scalars().first()
            return note

    @staticmethod
    async def get_all():
        async with db as session:
            stmt = select(Note)
            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def update(note_id: int, note_data: Note):
        async with db as session:
            stmt = select(Note).where(Note.id == note_id)
            result = await session.execute(stmt)

            note = result.scalars().first()
            if note:
                note.name = note_data.name
                note.description = note_data.description

                query = (
                    update(Note)
                    .where(Note.id == note_id)
                    .values(**note.dict())
                    .execution_options(synchronize_session="fetch")
                )

                await session.execute(query)
                await db.commit_rollback()

    @staticmethod
    async def delete(note_id: int):
        async with db as session:
            stmt = sql_delete(Note).where(Note.id == note_id)
            await session.execute(stmt)
            await db.commit_rollback()
