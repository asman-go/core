import pytest

from asman.domains.bugbounty_programs.repo import ProgramRepository
from asman.domains.bugbounty_programs.api import (
    ProgramId,
)


def test_program_repository_instance_create(db_in_memory):
    repo = ProgramRepository(db_in_memory)

    assert repo


@pytest.mark.asyncio
async def test_program_repository_insert(program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    program = await program_repository.get_by_id(ProgramId(id=program_id))

    assert program_id
    assert program
    assert isinstance(program_id, int)


@pytest.mark.asyncio
async def test_program_repository_update(program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    program = await program_repository.get_by_id(ProgramId(id=program_id))
    OLD_VALUE = program.data.notes
    program.data.notes += 'UPDATED'
    updated_program = await program_repository.update(program)

    assert updated_program
    assert updated_program.id.id == program_id
    assert updated_program.data.notes == OLD_VALUE + 'UPDATED'


@pytest.mark.asyncio
async def test_program_repository_get_by_id(program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    program = await program_repository.get_by_id(ProgramId(id=program_id))

    assert program
    assert program.id.id == program_id
    assert program.data.program_name == program_data.program_name


@pytest.mark.asyncio
async def test_program_repository_list(program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    programs = await program_repository.list()

    assert programs
    assert isinstance(programs, list)
    assert len(programs) > 0


@pytest.mark.asyncio
async def test_program_repository_delete(asset_repository, program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    id = ProgramId(id=program_id)
    program = await program_repository.get_by_id(id)

    await program_repository.delete(id)
    deleted_program = await program_repository.get_by_id(id)

    assets = await asset_repository.list(id)

    assert program_id, 'ProgramData was not inserted'
    assert program, 'Can not find the inserted program'
    assert not deleted_program, 'The program was not deleted'
    assert len(assets) == 0, 'Assets were not deleted'
