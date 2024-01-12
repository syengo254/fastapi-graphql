from models.user import User
from config import db
from sqlalchemy.sql import select
from sqlalchemy import update, delete as sql_delete


class UserRepository:
    @staticmethod
    async def create(user_data: User):
        async with db as session:
            async with session.begin():
                user_data.email = user_data.email.lower()
                session.add(user_data)
            await db.commit_rollback()
        return await UserRepository.get_by_email(user_data.email)

    @staticmethod
    async def get_by_id(user_id: int) -> User | None:
        async with db as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)
            user = result.scalars().first()
            return user

    @staticmethod
    async def get_by_email(email: str) -> User | None:
        async with db as session:
            stmt = select(User).where(User.email == email.lower())
            result = await session.execute(stmt)
            user = result.scalars().first()
            return user

    @staticmethod
    async def get_all():
        async with db as session:
            stmt = select(User)
            result = await session.execute(stmt)
            return result.scalars().all()

    @staticmethod
    async def update(user_id: int, user_data: User):
        async with db as session:
            stmt = select(User).where(User.id == user_id)
            result = await session.execute(stmt)

            user = result.scalars().first()
            if user:
                user.name = user_data.name
                user.description = user_data.description
                user_data.email = user_data.email.lower()

                query = (
                    update(User)
                    .where(User.id == user_id)
                    .values(**user.dict())
                    .execution_options(synchronize_session="fetch")
                )

                await session.execute(query)
                await db.commit_rollback()

    @staticmethod
    async def delete(user_id: int):
        async with db as session:
            stmt = sql_delete(User).where(User.id == user_id)
            await session.execute(stmt)
            await db.commit_rollback()
