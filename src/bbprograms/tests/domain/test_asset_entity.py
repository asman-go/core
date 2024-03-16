import pytest

from src.bbprograms.domain import (
    AssetEntity,
    InvalidAssetTypeException,
)


def test_asset_create():
    asset = AssetEntity(
        type='host',
        value='127.0.0.1',
        is_paid=False
    )

    assert asset
    assert asset.id
    assert asset.type == 'host'
    assert asset.value == '127.0.0.1'
    assert asset.is_paid == False


def test_asset_create_throws_invalid_type_exception():
    with pytest.raises(InvalidAssetTypeException) as exc:
        asset = AssetEntity(
            type='TOTALLY_INVALID',
            value='127.0.0.1',
            is_paid=False
        )

    assert isinstance(exc.value, InvalidAssetTypeException)
