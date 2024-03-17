from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    value: str = Field(alias='some_value')
