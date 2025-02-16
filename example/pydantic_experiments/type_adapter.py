import pydantic
import typing


class User(pydantic.BaseModel):
    name: str = pydantic.Field()


if __name__ == '__main__':
    users = [
        {
            'name': 'Ivan',
        },
        {
            'name': 'Egor'
        }
    ]

    validated_data = pydantic.TypeAdapter(typing.List[User]).validate_python(users)
    print(validated_data)
