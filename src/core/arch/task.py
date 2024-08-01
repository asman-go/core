from abc import ABC, abstractmethod
from collections.abc import Iterable
from functools import wraps
from pubsub import pub, core
import pydantic
import pydantic_settings
import typing


def error(function):

    @wraps(function)
    def wrapper(*argv, **kwargs):
        try:
            # print('error decorator', argv, kwargs)
            result = function(*argv, **kwargs)
            return result
        except Exception as ex:
            # TODO: Надо сохранить информацию об ошибке куда-нибудь
            print('error decorator', argv, kwargs, ex)

    return wrapper

def debug(function):

    @wraps(function)
    def wrapper(*argv, **kwargs):
        result = function(*argv, **kwargs)
        print('DEBUG', argv[0].__class__.__name__, kwargs, 'result:', result)
        return result

    return wrapper


class AbstractTask(core.listener.UserListener, ABC):
    config: pydantic_settings.BaseSettings
    topics: typing.Set[str]
 
    def __init__(
                self,
                *models: typing.Sequence[pydantic.BaseModel],
                config: pydantic_settings.BaseSettings | None = None
            ) -> None:

        self.config = config
        self.topics = set(map(
            # Использую название pydantic модели (класса) для названия топика
            lambda model: model.__name__,
            models,
        ))

        for topic in self.topics:
            pub.subscribe(
                self,  # task
                topic,  # topic name
            )

    @abstractmethod
    def _call(self, message: pydantic.BaseModel) -> pydantic.BaseModel | typing.Sequence[pydantic.BaseModel] | None:
        ...

    @error
    @debug
    def __call__(self, message: pydantic.BaseModel) -> None:
        res = self._call(message)
        print('Return from _call:', res)
        # Если список чего либо, то запускаем события, иначе одно событие
        if isinstance(res, Iterable):
            for item in res:
                SendTaskMessage(item)

        if res:
            SendTaskMessage(item)



class SendTaskMessage(object):
    def __init__(self, message: pydantic.BaseModel) -> None:
        print('Try to send', type(message).__name__)
        pub.sendMessage(
            type(message).__name__,  # topic name
            message=message,
        )


class TaskQueue(object):
    topics: typing.Set[str]

    def __init__(self, *tasks: typing.Sequence[AbstractTask]) -> None:
        self.topics = set()
        for task in tasks:
            self.topics.update(task.topics)

    def send(self, message: pydantic.BaseModel):
        topic = type(message).__name__
        if topic in self.topics:
            print('Send message', message)
            pub.sendMessage(topic, message=message)
        else:
            print('Topic not found', topic, self.topics)
