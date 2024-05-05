import pytest

from asman.domains.bugbounty_programs.use_cases import DeleteProgramUseCase


def test_delete_program_use_case_create():
    delete_use_case = DeleteProgramUseCase(None, None)

    assert delete_use_case, 'Use case is not created'
    assert delete_use_case.repo, 'Repo property not found'


@pytest.mark.asyncio
async def test_read_program_use_case_execute(
            create_program_use_case,
            delete_program_use_case,
            read_program_by_id_use_case,
            program_data
        ):
    programId = await create_program_use_case.execute(program_data)
    program = await read_program_by_id_use_case.execute(programId)
    res = await delete_program_use_case.execute(programId)
    deleted_program = await read_program_by_id_use_case.execute(programId)

    assert res, 'The use case was executed successfully'
    assert not deleted_program, 'The program was deleted'
