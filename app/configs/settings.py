from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_TYPE: str

    class Config:
        env_file = '.env'


settings = Settings()
