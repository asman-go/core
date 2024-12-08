import pytest

from asman.domains.bugbounty_programs.use_cases import AddAssetsUseCase
from asman.domains.bugbounty_programs.api import AddAssetsRequest


def test_add_assets_use_case_create_instance():
    use_case = AddAssetsUseCase(None, None)

    assert use_case, 'Use case is not created'
    assert use_case.repo, 'Repo property not found'


@pytest.mark.asyncio
async def test_add_assets_use_case_execute(read_program_by_id_use_case, create_program_use_case, add_assets_use_case, program_data, assets):
    program_id = await create_program_use_case.execute(program_data)

    assert program_id
    assert isinstance(program_id, int)

    await add_assets_use_case.execute(
        AddAssetsRequest(
            program_id=program_id,
            assets=assets
        )
    )

    program = await read_program_by_id_use_case.execute(program_id)
    for asset in assets:
        assert asset in program.data.assets
