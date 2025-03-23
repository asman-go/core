import pytest
import pytest_asyncio

from asman.domains.bugbounty_programs.api import Program, SearchByID
from asman.domains.bugbounty_programs.use_cases import UpdateProgramUseCase


@pytest_asyncio.fixture
async def program_id(program_repository, new_program):
    ids = await program_repository.insert([new_program])

    return ids[0].program_id


@pytest.mark.asyncio
async def test_update_program_use_case_execute(
            update_program_use_case: UpdateProgramUseCase,
            program_repository,
            program_id,
        ):

    programs = await program_repository.search([SearchByID(id=program_id)])
    program = programs[0]
    program_to_update = program.model_copy(deep=True)
    program_to_update.program_name = 'SOME_NEW_VALUE'

    _updated_program_id = await update_program_use_case.execute(program_to_update)
    programs = await program_repository.search([SearchByID(id=program_id)])

    assert _updated_program_id
    assert _updated_program_id.program_id == program_to_update.id
    assert programs[0].program_name == 'SOME_NEW_VALUE'
