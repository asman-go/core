from abc import ABC, abstractmethod
from pydantic_settings import BaseSettings


class AbstractUseCase(ABC):
    @abstractmethod
    def __init__(self, config: BaseSettings, *argv) -> None:
        ...

    @abstractmethod
    def execute(self, request):
        ...
