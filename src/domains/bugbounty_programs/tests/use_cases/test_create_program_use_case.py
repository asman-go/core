import pytest

from asman.domains.bugbounty_programs.use_cases import CreateProgramUseCase


def test_create_program_use_case_instance_create():
    use_case = CreateProgramUseCase(None, None)

    assert use_case, 'Use case is not created'
    assert use_case.repo, 'Repo property not found'


@pytest.mark.asyncio
async def test_create_program_use_case_execute(create_program_use_case: CreateProgramUseCase, program_data):
    program_id = await create_program_use_case.execute(program_data)

    assert program_id
    assert isinstance(program_id, int)


@pytest.mark.asyncio
async def test_create_program_use_case_execute2(create_program_use_case: CreateProgramUseCase, program_data, program_data_other):
    program_id1 = await create_program_use_case.execute(program_data)
    program_id2 = await create_program_use_case.execute(program_data)

    assert program_id1
    assert program_id2
    assert isinstance(program_id1, int)
    assert isinstance(program_id2, int)
    assert program_id1 == program_id2

    program_id3 = await create_program_use_case.execute(program_data_other)
    assert program_id3
    assert isinstance(program_id3, int)
    assert program_id1 != program_id3
