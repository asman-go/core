import pytest
import pytest_asyncio

from asman.domains.bugbounty_programs.use_cases import RemoveAssetsUseCase
from asman.domains.bugbounty_programs.api import ProgramId, NewLinkedAsset


@pytest_asyncio.fixture
async def program_id(program_repository, new_program) -> ProgramId:
    ids = await program_repository.insert([new_program])

    return ids[0]


@pytest.mark.asyncio
async def test_remove_assets_use_case_execute(remove_assets_use_case: RemoveAssetsUseCase, program_id: ProgramId, asset_repository, new_assets):
    ids = await asset_repository.insert(list(
        map(
            lambda new_asset: NewLinkedAsset(
                program_id=program_id.program_id,
                **new_asset.model_dump(),
            ),
            new_assets,
        )
    ))

    asset_id1 = ids[0]

    # Удаляем 1 ассет
    removed_asset_ids = await remove_assets_use_case.execute(asset_id1)

    assert removed_asset_ids and len(removed_asset_ids) == 1
    assert removed_asset_ids[0].id == asset_id1.id

    # Удаляем все ассеты по program id
    removed_asset_ids = await remove_assets_use_case.execute(program_id)
    assert removed_asset_ids and len(removed_asset_ids) > 1

    # Пробую удалить ассет, которого нет
    removed_asset_ids = await remove_assets_use_case.execute(asset_id1)
    assert len(removed_asset_ids) == 0

    # Пробую удалить ассеты по программе, для которой нет ассетов
    removed_asset_ids = await remove_assets_use_case.execute(program_id)
    assert len(removed_asset_ids) == 0

    # Пробую удалить ассеты по несуществующей программе
    removed_asset_ids = await remove_assets_use_case.execute(ProgramId(program_id=1241234512))
    assert len(removed_asset_ids) == 0
