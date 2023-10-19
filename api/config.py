from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RABBITMQ_USER: str = 'username'
    RABBITMQ_PASS: str = 'password'
    RABBITMQ_HOST: str = '127.0.0.1'

    @property
    def get_amqp_url(self):
        return (
            f'amqp://{self.RABBITMQ_USER}:'
            f'{self.RABBITMQ_PASS}@{self.RABBITMQ_HOST}/'
        )

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )


settings = Settings()
