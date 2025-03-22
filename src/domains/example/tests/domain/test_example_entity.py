import pytest

from asman.domains.example.domain import ExampleData
from asman.domains.example.domain import ExampleException


def test_example_data_create():
    ADDRESS_VALUE = '123456'
    entity = ExampleData(
        id='1',
        address=ADDRESS_VALUE
    )

    assert entity
    assert entity.address
    assert entity.address == ADDRESS_VALUE


def test_example_data_create_throws_example_exception():
    with pytest.raises(ExampleException) as exc:
        ExampleData(
            id='1',
            address='1'
        )

    assert isinstance(exc.value, ExampleException)
