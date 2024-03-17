import pytest

from asman.domains.example.domain.example_entity import ExampleEntity
from asman.domains.example.domain.exceptions import ExampleException


def test_example_entity_create():
    ADDRESS_VALUE = '123456'
    entity = ExampleEntity(
        address=ADDRESS_VALUE
    )

    assert entity
    assert entity.address
    assert entity.address == ADDRESS_VALUE


def test_example_entity_create_throws_example_exception():
    with pytest.raises(ExampleException) as exc:
        ExampleEntity(
            address='1'
        )

    assert isinstance(exc.value, ExampleException)
