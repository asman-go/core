from abc import ABC
import typing
import pydantic


class T(object):
    _a: str | None

    def __init__(self, a: str | None = None):
        self._a = a

    def _init(self, func):
        def wrapper(*args, **kwargs):
            print('ARGS', args)
            result = func(*args, **kwargs)
            return result
        return wrapper

    @property
    def method(self, *argv):
        return self._init(self._method)

    def _method(self, *args):
        print('A', self._a)


class Table(pydantic.BaseModel):
    a: str = pydantic.Field()


class MetaData:
    _instance = None
    tables: typing.Dict[str, Table]

    def __new__(cls):
        # Singletone
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):
        self.tables = dict()


class DeclarativeBase(type):

    def __new__(cls, *args, **kwargs):
        # Создаем класс
        # new_class = super().__new__(cls, classname, bases, dict_)

        print('Parent __new__', cls)
        print('Parent __new__', args)
        print('Parent __new__', kwargs)

        # Создаем класс
        # new_class = super().__new__(cls, classname, bases, dict_)
        # print('Parent __new__', dir(new_class))

        # self = super().__new__(cls, classname, bases, dict_)
        self = super().__new__(cls, *args, **kwargs)

        print('Parent __new__', self)

        if hasattr(self, '__tablename__') and hasattr(self, '__a__'):
            MetaData().tables[getattr(self, '__tablename__')] = Table(a=getattr(self, '__a__'))

        return self


class MetaBase(metaclass=DeclarativeBase):
    metadata: MetaData = MetaData()


class Child(MetaBase):
    __tablename__: str = 'test1'
    __a__: str = 'a'


if __name__ == '__main__':
    # t = T(a="test")
    # t.method()
    # t.method("test2")
    # print(Child.metadata.tables)
    meta = MetaBase()
    print(meta.metadata.tables)
    # print(Child.metadata.tables)
