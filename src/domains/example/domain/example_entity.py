import pydantic

from core.arch import Entity

from .exceptions import ExampleException


class ExampleEntity(Entity):
    address: str

    @pydantic.field_validator('address')
    def address_validator(cls, value):
        if len(value) < 3:
            raise ExampleException

        return value
