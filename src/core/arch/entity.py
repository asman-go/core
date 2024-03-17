import pydantic
import uuid


class Entity(pydantic.BaseModel):
    """
        Модель для Database и бизнес модели
    """
    id: uuid.UUID = pydantic.Field(default_factory=lambda: uuid.uuid4())


class BusinessEntity(pydantic.BaseModel):
    """
        Сущность для бизнес модели
    """
    ...


class RequestEntity(pydantic.BaseModel):
    """
        Сущность для UseCase слоя
    """
    ...
