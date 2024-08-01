from abc import ABC, abstractmethod
from functools import wraps
import pydantic
from typing import Any
from asman.core import SendTaskMessage, TaskQueue
from asman.tasks import Task, WildcardDomainFormatTask, PlaygroundTask, DomainResolveTask
from asman.tasks.models import WildcardDomain, Domain


def main1():
    tasks = [
        PlaygroundTask(Task.TEST),
        DomainResolveTask(Task.DOMAIN),
        WildcardDomainFormatTask(Task.WILDCARD),
    ]
    # TODO: SendTaskMessage должен определять топики по типу сообщения => если надо, он сам отправит в несколько топиков
    # SendTaskMessage(Task.TEST, Domain(domain='test1'))
    # SendTaskMessage(Task.WILDCARD, WildcardDomain(domain='*.google.com'))

    # input('test')


def main2():
    tasks = [
        PlaygroundTask(Domain),
        DomainResolveTask(Domain),
    ]
    SendTaskMessage(Domain(domain='example.com'))
    # print(type(Domain(domain='str')).__name__)


def main3():
    # Какая та херота, таски обязательно должны быть в главном контексте
    tasks = [
        PlaygroundTask(Domain),
        DomainResolveTask(Domain),
        WildcardDomainFormatTask(WildcardDomain),
    ]
    queue = TaskQueue(*tasks)
    queue.send(WildcardDomain(domain='*.example.com'))

def error(function):

    @wraps(function)
    def wrapper(*argv, **kwargs):
        try:
            print('error decorator', argv, kwargs)
            result = function(*argv, **kwargs)
            return result
        except Exception as ex:
            # TODO: Надо сохранить информацию об ошибке куда-нибудь
            print('error decorator', argv, kwargs, ex)

    return wrapper


class AbstractA(object):
    @abstractmethod    
    def _call(self, *args: Any, **kwds: Any) -> Any:
        ...

    @error
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self._call(*args, *kwds)

class A(AbstractA):

    def _call(self, *args: Any, **kwds: Any) -> Any:
        print('test', self.__class__.__name__)


if __name__ == '__main__':
    main3()
    class TTT(pydantic.BaseModel):
        a: str

    SendTaskMessage(TTT(a='test'))
    # A()()
