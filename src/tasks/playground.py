from functools import wraps

from asman.core.arch import AbstractTask

from .models import Domain


def check(function):

    @wraps(function)
    def wrapper(*argv, **kwargs):
        print('check decorator', argv, kwargs)
        return function(*argv, **kwargs)

    return wrapper


def timeout(seconds: int):
    def decorator(function):

        @wraps(function)
        def wrapper(*argv, **kwargs):
            print('timeout decorator', argv, kwargs, 'seconds', seconds)
            return function(*argv, **kwargs)

        return wrapper

    return decorator


def saveto(name: str):
    def decorator(function):

        @wraps(function)
        def wrapper(*argv, **kwargs):
            result = function(*argv, **kwargs)
            print('saveto decorator', 'name:', name, 'args:', argv, kwargs, 'result:', result)
            return result

        return wrapper

    return decorator


class PlaygroundTask(AbstractTask):
    @check
    @timeout(5)
    @saveto('mongo')
    def _call(self, message: Domain):
        print('Message', self.config, message)
