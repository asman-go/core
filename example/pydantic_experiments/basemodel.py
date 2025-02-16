import functools
from pydantic import BaseModel, Field
from typing import Optional, List


class Cat(BaseModel):
    name: str = Field()
    friends: List['Cat'] = Field(default_factory=lambda: list())
    master_name: Optional[str] = Field(default=None)


if __name__ == '__main__':
    cat1 = Cat(name='Barsik', master_name='Oleg')
    cat2 = Cat(name='Druzhok', friends=[cat1])

    print('Cat 1', cat1.model_dump(exclude_unset=True).keys())
    print('Cat 2', cat2.model_dump(exclude_unset=True).keys())

    items = [1, 2, 3, 4, 5]
    items = [1, 2]
    items = [1]
    print(functools.reduce(
        lambda x, y: x + y,
        items
    ))
