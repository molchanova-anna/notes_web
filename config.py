from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings

# Helper for avoiding problem with path to 'env
load_dotenv(find_dotenv(".env"))

class Config(BaseSettings):
    DB_NAME: str
    DB_PASSWORD: str
    DB_USERNAME: str
    DB_HOST: str
    DB_PORT: str
    DB_CREATOR_USER: str = ''
    DB_CREATOR_PASSWORD: str = ''

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if 'env_file' in kwargs:
            self.Config.env_file = kwargs['env_file']

    def sqlalchemy_database_url(self, db_name: str = None):
        return f'postgresql+asyncpg://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{db_name or self.DB_NAME}'


config = Config()