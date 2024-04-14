import pytest
from asman.core.adapters.db import Postgres
from asman.core.exceptions import NotImplementedException


def test_postgres_instance_create(postgres_config):
    postgres = Postgres(postgres_config)

    assert postgres


def test_postgres_upsert_throws_not_implemented_exception(postgres):
    # upsert
    with pytest.raises(NotImplementedException) as exc:
        postgres.upsert('test', None)
    
    assert isinstance(exc.value, NotImplementedException)

    # get_item
    with pytest.raises(NotImplementedException) as exc:
        postgres.get_item('test', 1)

    assert isinstance(exc.value, NotImplementedException)
