from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.models import Base
from settings import Settings
import asyncpg, asyncio

settings = Settings()

username = settings.DB_USERNAME
password = settings.DB_PASSWORD
dbname = settings.DB_NAME
db_port = settings.DB_PORT
db_host = settings.DB_HOST
db_creator_user = settings.DB_CREATOR_USER
db_creator_password = settings.DB_CREATOR_PASSWORD

SQLALCHEMY_DATABASE_URL = f"postgresql+asyncpg://{username}:{password}@{db_host}:{db_port}/{dbname}"

async def create_db():
    need_create_db = False
    try:
        conn = await asyncpg.connect(user=username, database=dbname, password=password)
        await conn.close()
    except asyncpg.InvalidCatalogNameError:
        need_create_db = True
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database='template1',
            user=db_creator_user,
            password=db_creator_password,
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{dbname}" OWNER "{username}"'
        )
        await sys_conn.close()

        # Connect to the newly created database.
        async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
        if need_create_db:
            async with async_engine.begin() as connect:
                await connect.run_sync(Base.metadata.create_all)

asyncio.get_event_loop().run_until_complete(
    create_db()
)
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False, autocommit=False)