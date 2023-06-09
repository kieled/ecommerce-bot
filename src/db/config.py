from config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

DATABASE_URL = (
    f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}"
    f"@{settings.POSTGRES_HOST}"
    f":{settings.POSTGRES_PORT}"
    f"/{settings.POSTGRES_DB}"
)

engine = create_async_engine(DATABASE_URL)

session = async_sessionmaker(engine, expire_on_commit=False, autoflush=False, autocommit=False)
