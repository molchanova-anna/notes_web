'''
Connection to DB
'''

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker

from database.models import Base
from config import config as db_config
import asyncpg, asyncio

SQLALCHEMY_DATABASE_URL = db_config.sqlalchemy_database_url()

async def create_db():
    try:
        conn = await asyncpg.connect(host=db_config.DB_HOST,
                                     port=db_config.DB_PORT,
                                     user=db_config.DB_USERNAME,
                                     database=db_config.DB_NAME,
                                     password=db_config.DB_PASSWORD)
        await conn.close()
    except asyncpg.InvalidCatalogNameError:
        # Database does not exist, create it.
        sys_conn = await asyncpg.connect(
            database='template1',
            user=db_config.DB_CREATOR_USER,
            password=db_config.DB_CREATOR_PASSWORD,
        )
        await sys_conn.execute(
            f'CREATE DATABASE "{db_config.DB_NAME}" OWNER "{db_config.DB_USERNAME}"'
        )
        await sys_conn.close()

        # Connect to the newly created database.
        async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
        async with async_engine.begin() as connect:
            await connect.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(
        create_db()
    )
async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)
async_session = async_sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False, autocommit=False)