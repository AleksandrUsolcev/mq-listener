from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    RABBITMQ_USER: str = 'username'
    RABBITMQ_PASS: str = 'password'
    RABBITMQ_HOST: str = '127.0.0.1'
    RABBITMQ_QUEUE_NAME: str = 'queue_name'

    API_HOST: str = '127.0.0.1'
    API_PORT: int = 8000

    WS_HOST: str = '127.0.0.1'
    WS_PORT: int = 8001

    CONSUMER_RECONNECT_TIMEOUT: int = 5

    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = 6379

    RABBITMQ_RECONNECT_TIMEOUT: int = 30

    @property
    def get_amqp_url(self):
        return (
            f'amqp://{self.RABBITMQ_USER}:'
            f'{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}/'
        )

    @property
    def get_ws_url(self):
        return f'ws://{self.WS_HOST}:{self.WS_PORT}/listen_results'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


settings = Settings()
