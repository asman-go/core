import copy
import pytest

from asman.domains.bugbounty_programs.api import Program
from asman.domains.bugbounty_programs.use_cases import UpdateProgramUseCase


def test_update_program_use_case_instance_create():
    update_use_case = UpdateProgramUseCase(None, None)

    assert update_use_case, 'Use case is not created'
    assert update_use_case.repo, 'Repo property not found'


@pytest.mark.asyncio
async def test_update_program_use_case_execute(
            create_program_use_case,
            update_program_use_case,
            program_data
        ):

    program_id = await create_program_use_case.execute(program_data)

    copy_program_data = copy.deepcopy(program_data)
    copy_program_data.program_name = 'SOME_NEW_VALUE'

    updated_program = await update_program_use_case.execute(
        Program(
            id=program_id,
            data=copy_program_data,
        )
    )

    assert updated_program
    assert updated_program.id == program_id
    assert updated_program.data.program_name == 'SOME_NEW_VALUE'
