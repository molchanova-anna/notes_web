from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_NAME: str
    DB_PASSWORD: str
    DB_USERNAME: str
    DB_HOST: str
    DB_PORT: str
    DB_CREATOR_USER: str = ''
    DB_CREATOR_PASSWORD: str = ''

    class Config:
        env_file = ".env"

    def __init__(self, **kwargs): # TODO
        super().__init__(**kwargs)
        if 'env_file' in kwargs:
            self.Config.env_file = kwargs['env_file']