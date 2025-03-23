import pytest
import pytest_asyncio

from asman.domains.bugbounty_programs.api import SearchByID
from asman.domains.bugbounty_programs.use_cases import DeleteProgramUseCase


@pytest_asyncio.fixture
async def program_id(program_repository, new_program):
    ids = await program_repository.insert([new_program])

    return ids[0].program_id


@pytest.mark.asyncio
async def test_delete_program_use_case_execute(delete_program_use_case: DeleteProgramUseCase, program_repository, program_id):
    _deleted_program_id = await delete_program_use_case.execute(SearchByID(id=program_id))

    assert program_id == _deleted_program_id.program_id

    program = await program_repository.search([SearchByID(id=_deleted_program_id.program_id)])

    assert len(program) == 0

    # Пробую удалить несуществующую программу -> Exception
    # _deleted_program_id = await delete_program_use_case.execute(SearchByID(id=1241351325))
    # assert _deleted_program_id == 1
