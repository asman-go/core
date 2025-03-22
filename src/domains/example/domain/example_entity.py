from pydantic import BaseModel, Field, field_validator

from .exceptions import ExampleException


class ExampleData(BaseModel):
    id: str = Field()
    address: str = Field()

    @field_validator('address')
    def address_validator(cls, value):
        if len(value) < 3:
            raise ExampleException

        return value


class ExampleEntity(ExampleData):...
