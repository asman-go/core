import pytest

from asman.domains.bugbounty_programs.api import (
    Asset,
    AssetType,
)
from asman.domains.bugbounty_programs.repo import AssetRepository


def test_asset_repository_instance_create(db_in_memory):
    repo = AssetRepository(db_in_memory)

    assert repo


@pytest.fixture
async def programId(program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    return program_id


@pytest.mark.asyncio
async def test_asset_repository_insert_and_list(programId, assets, asset_repository):
    programId = await programId
    await asset_repository.insert(programId, assets)

    all_assets = await asset_repository.list(programId)

    assert all_assets, 'No assets were added'
    assert isinstance(all_assets, list), 'Wrong assets\' type'
    assert len(all_assets) >= len(assets), 'Wrong assets\' amount'


@pytest.mark.asyncio
async def test_asset_repository_delete(programId, assets, asset_repository):
    programId = await programId
    await asset_repository.insert(programId, assets)
    old_all_assets = await asset_repository.list(programId)
    await asset_repository.delete(programId, assets)
    new_all_assets = await asset_repository.list(programId)

    assert len(new_all_assets) < len(old_all_assets), 'There are more assets left than expected'
