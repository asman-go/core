import pytest
import pytest_asyncio

from asman.domains.bugbounty_programs.api import NewLinkedAsset


@pytest_asyncio.fixture
async def new_program_id(asset_repository, program_repository, new_program, new_assets):
    ids = await program_repository.insert([new_program])
    program_id = ids[0].program_id
    await asset_repository.insert(list(
        map(
            lambda new_asset: NewLinkedAsset(
                program_id=program_id,
                **new_asset.model_dump(),
            ),
            new_assets,
        )
    ))
    return ids[0]


@pytest.mark.asyncio
async def test_get_assets_use_case_execute(get_assets_use_case, new_program_id):
    assets = await get_assets_use_case.execute(new_program_id)

    assert assets
    assert len(assets) > 0
