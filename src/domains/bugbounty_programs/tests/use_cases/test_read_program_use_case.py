import pytest
import pytest_asyncio

from asman.domains.bugbounty_programs.use_cases import (
    ReadProgramUseCase,
    ReadProgramByIdUseCase,
)
from asman.domains.bugbounty_programs.api import SearchByID


@pytest_asyncio.fixture
async def program_id(program_repository, new_program):
    ids = await program_repository.insert([new_program])

    return ids[0]


@pytest.mark.asyncio
async def test_read_program_use_case_execute(
            read_program_use_case: ReadProgramUseCase,
            read_program_by_id_use_case: ReadProgramByIdUseCase,
            program_id
        ):
    programs = await read_program_use_case.execute()

    assert len(programs) > 0

    program = await read_program_by_id_use_case.execute(SearchByID(id=program_id.program_id))

    assert program
    assert program_id.program_id == program.id
