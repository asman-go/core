import pytest

from asman.domains.bugbounty_programs.use_cases import RemoveAssetsUseCase
from asman.domains.bugbounty_programs.api import RemoveAssetsRequest, AddAssetsRequest


def test_remove_assets_use_case_create_instance():
    use_case = RemoveAssetsUseCase(None, None)

    assert use_case, 'Use case is not created'
    assert use_case.repo, 'Repo property not found'


@pytest.mark.asyncio
async def test_remove_assets_use_case_execute(read_program_by_id_use_case, create_program_use_case, add_assets_use_case, remove_assets_use_case, program_data, assets):
    program_id = await create_program_use_case.execute(program_data)
    await add_assets_use_case.execute(
        AddAssetsRequest(
            program_id=program_id,
            assets=assets
        )
    )
    await remove_assets_use_case.execute(
        RemoveAssetsRequest(
            program_id=program_id,
            assets=[assets[0]]
        )
    )

    program = await read_program_by_id_use_case.execute(program_id)
    assert assets[0] not in program.data.assets

    for asset in assets[1:]:
        assert asset in program.data.assets
