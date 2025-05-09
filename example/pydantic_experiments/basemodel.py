import functools
from pydantic import BaseModel, Field, create_model, TypeAdapter
from typing import Optional, List, Dict, Any


class Cat(BaseModel):
    name: str = Field()
    friends: List['Cat'] = Field(default_factory=lambda: list())
    master_name: Optional[str] = Field(default=None)


def optional_fields():
    cat1 = Cat(name='Barsik', master_name='Oleg')
    cat2 = Cat(name='Druzhok', friends=[cat1])

    print('Cat 1', cat1.model_dump(exclude_unset=True).keys())
    print('Cat 2', cat2.model_dump(exclude_unset=True).keys())


def basemodel_type_casting():
    def func(cat: BaseModel):
        print('Cat', cat.model_dump())

    obj = {'master_name': 'test'}
    obj = TypeAdapter(Dict[str, Any]).validate_python(obj)
    _Req = create_model('Req', master_name=(str, ...))
    obj = _Req(**obj)
    # obj = BaseModel(**obj)
    func(obj)


def get_fields():
    cat1 = Cat(name='Barsik', master_name='Oleg')
    fields = cat1.model_fields.keys()
    s = ['id', 'name', 'test']
    print(fields & s)


def basemodel_as_protocol():
    class A(BaseModel):
        a: str = Field()

    class B(BaseModel):
        b: str = Field()

    def t(a: A):
        if a.a == 'test':
            print('basemodel_as_protocol', a.a)
        else:
            print('basemodel_as_protocol', 'fail')

    a = A(a='test')
    t(a)


def inheritance():
    class A(BaseModel):
        a: str

        def __eq__(self, value: 'A'):
            print('Вот так')
            return self.a == value.a

    class B(A):
        b: str

    a = B(a='1', b='2')
    b = B(a='2', b='2')

    print('Как сравниваются объекты с наследованием?', a == b)


if __name__ == '__main__':
    # optional_fields()
    # basemodel_type_casting()
    # get_fields()
    # basemodel_as_protocol()
    inheritance()
