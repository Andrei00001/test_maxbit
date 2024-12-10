from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    BOT_TOKEN: str
    API_ID: str
    API_HASH: str
    NAME_BOT: str = 'TestMaxbit'

    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file=ROOT_DIR / '.env', extra='ignore')

    @property
    def DATABASE_URI_WITH_DRIVER(self) -> str:
        return self.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')


settings = Settings()
