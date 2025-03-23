import pytest

from asman.domains.bugbounty_programs.use_cases import CreateProgramUseCase


@pytest.mark.asyncio
async def test_create_program_use_case_execute(create_program_use_case: CreateProgramUseCase, new_program):
    program_id = await create_program_use_case.execute(new_program)

    assert program_id
    assert isinstance(program_id.program_id, int)


@pytest.mark.asyncio
async def test_create_program_use_case_execute2(create_program_use_case: CreateProgramUseCase, new_program, new_program_other):
    program_id1 = await create_program_use_case.execute(new_program)
    program_id2 = await create_program_use_case.execute(new_program)

    assert program_id1
    assert program_id2
    assert program_id1.program_id == program_id2.program_id

    program_id3 = await create_program_use_case.execute(new_program_other)
    assert program_id3
    assert program_id1.program_id != program_id3.program_id
