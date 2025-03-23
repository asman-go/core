import pytest

from asman.domains.bugbounty_programs.api import (
    Asset,
    NewLinkedAsset,
    AssetType,
)
from asman.domains.bugbounty_programs.repo import AssetRepository


def test_asset_repository_instance_create(database, asset_table_name):
    repo = AssetRepository(database, asset_table_name)

    assert repo
    assert repo.database
    assert repo.table_name == asset_table_name


@pytest.fixture
async def program_id(program_repository, new_program):
    ids = await program_repository.insert([new_program])

    return ids[0].program_id


@pytest.mark.asyncio
async def test_asset_repository_crud(asset_repository, new_assets, program_id):
    _program_id = await program_id
    ids = await asset_repository.insert(list(
        map(
            lambda new_asset: NewLinkedAsset(
                program_id=_program_id,
                **new_asset.model_dump(),
            ),
            new_assets,
        )
    ))

    assert ids and len(ids) == len(new_assets)

    assets = await asset_repository.search(ids)
    assert assets and len(assets) == len(new_assets)

    for asset in assets:
        assert asset in new_assets

    assets = await asset_repository.list()
    assert assets and len(assets) == len(new_assets)

    ids = await asset_repository.delete([ids[0]])
    assert ids and len(ids) == 1
