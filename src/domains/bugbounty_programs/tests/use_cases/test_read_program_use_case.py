import pytest

from asman.domains.bugbounty_programs.use_cases import (
    ReadProgramUseCase,
    ReadProgramByIdUseCase,
)


def test_read_program_use_case_instance_create():
    read_use_case = ReadProgramUseCase(None, None)
    read_by_id_use_case = ReadProgramByIdUseCase(None, None)

    assert read_use_case, 'Use case is not created'
    assert read_use_case.repo, 'Repo property not found'

    assert read_by_id_use_case, 'Use case is not created'
    assert read_by_id_use_case.repo, 'Repo property not found'


@pytest.mark.asyncio
async def test_read_program_use_case_execute(
            read_program_use_case,
            read_program_by_id_use_case,
            create_program_use_case,
            program_data
        ):
    program_id_1 = await create_program_use_case.execute(program_data)
    await create_program_use_case.execute(program_data)

    programs = await read_program_use_case.execute()

    assert len(programs) > 1

    program = await read_program_by_id_use_case.execute(program_id_1)

    assert program
    assert program_id_1.id == program.id.id
    assert program_data.program_name == program.data.program_name
    assert program_data.program_site == program.data.program_site
    assert program_data.platform == program.data.platform
    assert len(program_data.assets) == len(program.data.assets)
    assert program_data.notes == program.data.notes
