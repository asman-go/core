import pydantic
import uuid


class Entity(pydantic.BaseModel):
    """
        Модель для Database и бизнес модели
    """
    id: str = pydantic.Field(default_factory=lambda: str(uuid.uuid4()))


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
