from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    WS_HOST: str = '127.0.0.1'
    WS_PORT: int = 8001

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


settings = Settings()
