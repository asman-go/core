import pytest
import pytest_asyncio

from asman.domains.bugbounty_programs.use_cases import AddAssetsUseCase
from asman.domains.bugbounty_programs.api import AddAssetsRequest


@pytest_asyncio.fixture
async def program_id(program_repository, new_program):
    ids = await program_repository.insert([new_program])

    return ids[0].program_id


@pytest.mark.asyncio
async def test_add_assets_use_case_execute(add_assets_use_case, program_id, new_assets):
    ids = await add_assets_use_case.execute(
        AddAssetsRequest(
            program_id=program_id,
            assets=new_assets,
        )
    )

    assert ids
    assert len(ids) == len(new_assets)
