import pytest


from asman.domains.bugbounty_programs.use_cases import CreateProgramUseCase


@pytest.fixture
def create_program_use_case():
    use_case = CreateProgramUseCase(None, None)

    return use_case


def test_create_program_use_case_instance_create():
    use_case = CreateProgramUseCase(None, None)

    assert use_case
    assert use_case.repo


@pytest.mark.asyncio
async def test_create_program_use_case_execute(create_program_use_case: CreateProgramUseCase, create_program_request):
    program_id = await create_program_use_case.execute(create_program_request)

    assert program_id
    assert isinstance(program_id, int)


@pytest.mark.asyncio
async def test_create_program_use_case_execute2(create_program_use_case: CreateProgramUseCase, create_program_request):
    program_id1 = await create_program_use_case.execute(create_program_request)
    program_id2 = await create_program_use_case.execute(create_program_request)

    assert program_id1
    assert program_id2
    assert isinstance(program_id1, int)
    assert isinstance(program_id2, int)
    assert program_id1 != program_id2


