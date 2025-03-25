from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)


async def get_user(db: AsyncSession, user_id: int):
    query = text("SELECT * FROM users WHERE id = :user_id;")
    result = await db.execute(query, {"user_id": user_id})
    users = result.mappings().all()
    return [dict(user) for user in users]



async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100):
    try:
        query = text("SELECT * FROM users LIMIT :limit OFFSET :skip;")
        result = await db.execute(query, {"limit": limit, "skip": skip})
        users = result.mappings().all()
        print(users)
        # return [dict(user) for user in users]
    except Exception as e:
        logger.error(f"Error executing SQL query: {e}")
        raise e


async def create_user(db: AsyncSession, user):
    try:
        query = text("INSERT INTO users (name, email) VALUES (:name, :email);")
        await db.execute(query, {"name": user.name, "email": user.email})
        await db.commit()
        return {"message": "User created successfully"}
    except Exception as e:
        logger.error(f"Error executing SQL query: {e}")
        await db.rollback()
        raise e
