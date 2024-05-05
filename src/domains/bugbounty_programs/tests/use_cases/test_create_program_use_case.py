import pytest

from asman.domains.bugbounty_programs.api import ProgramId
from asman.domains.bugbounty_programs.use_cases import CreateProgramUseCase


def test_create_program_use_case_instance_create():
    use_case = CreateProgramUseCase(None, None)

    assert use_case
    assert use_case.repo


@pytest.mark.asyncio
async def test_create_program_use_case_execute(create_program_use_case: CreateProgramUseCase, program_data):
    program_id = await create_program_use_case.execute(program_data)

    assert program_id
    assert isinstance(program_id, ProgramId)


@pytest.mark.asyncio
async def test_create_program_use_case_execute2(create_program_use_case: CreateProgramUseCase, program_data):
    program_id1 = await create_program_use_case.execute(program_data)
    program_id2 = await create_program_use_case.execute(program_data)

    assert program_id1
    assert program_id2
    assert isinstance(program_id1, ProgramId)
    assert isinstance(program_id2, ProgramId)
    assert program_id1 != program_id2
