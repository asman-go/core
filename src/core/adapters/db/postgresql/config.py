import pydantic
from pydantic_settings import BaseSettings


class PostgresConfig(BaseSettings):
    POSTGRES_DB: str = pydantic.Field(default='my_db')
    POSTGRES_USER: str = pydantic.Field(default='my_user')
    POSTGRES_PASSWORD: str = pydantic.Field(default='my_password')
    POSTGRES_HOST: str = pydantic.Field(
        default='localhost'
    )
    POSTGRES_PORT: int = pydantic.Field(
        default=5432
    )
