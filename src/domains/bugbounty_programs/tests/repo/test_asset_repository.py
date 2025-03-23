import pytest
import pytest_asyncio

from asman.domains.bugbounty_programs.api import (
    NewLinkedAsset,
)
from asman.domains.bugbounty_programs.repo import AssetRepository


def test_asset_repository_instance_create(database, asset_table_name):
    repo = AssetRepository(database, asset_table_name)

    assert repo
    assert repo.database
    assert repo.table_name == asset_table_name


@pytest_asyncio.fixture
async def program_id(program_repository, new_program):
    ids = await program_repository.insert([new_program])

    return ids[0]


@pytest.mark.asyncio
async def test_asset_repository_crud(asset_repository, new_assets, program_id):
    ids = await asset_repository.insert(list(
        map(
            lambda new_asset: NewLinkedAsset(
                program_id=program_id.program_id,
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


@pytest.fixture
async def test_asset_repository_delete_by_program_id(asset_repository, new_assets, program_id):
    ids = await asset_repository.insert(list(
        map(
            lambda new_asset: NewLinkedAsset(
                program_id=program_id.program_id,
                **new_asset.model_dump(),
            ),
            new_assets,
        )
    ))

    assert ids and len(ids) == len(new_assets)

    ids = await asset_repository.delete([program_id])
    assert ids and len(ids) == len(new_assets)

    assets = await asset_repository.search([program_id])
    assert len(assets) == 0
