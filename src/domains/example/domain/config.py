from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    value: str = Field(alias='some_value')
