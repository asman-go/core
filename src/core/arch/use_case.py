from abc import ABC, abstractmethod
from pydantic_settings import BaseSettings
from typing import Optional


class AbstractUseCase(ABC):
    @abstractmethod
    def __init__(self, config: Optional[BaseSettings] = None, *argv) -> None:
        ...

    @abstractmethod
    def execute(self, request):
        ...
