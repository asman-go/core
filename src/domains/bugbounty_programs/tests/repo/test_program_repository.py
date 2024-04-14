import pytest

from asman.domains.bugbounty_programs.repo import ProgramRepository


def test_program_repository_instance_create(db_in_memory):
    repo = ProgramRepository(db_in_memory)

    assert repo


@pytest.mark.asyncio
async def test_program_repository_insert(program_repository, create_program_request):
    program_id = await program_repository.insert(create_program_request)

    assert program_id
    assert isinstance(program_id, int)
