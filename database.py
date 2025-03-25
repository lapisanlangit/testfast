
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from settings import settings
# MySQL connection URL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Create the SQLAlchemy engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL)


# Create an AsyncSessionLocal class for database sessions
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# Dependency to get the async database session


async def get_db():
    async with AsyncSessionLocal() as db:
        yield db
