import pytest

from asman.domains.bugbounty_programs.repo import ProgramRepository


def test_program_repository_instance_create(db_in_memory):
    repo = ProgramRepository(db_in_memory)

    assert repo, 'No repo in ProgramRepository'


@pytest.mark.asyncio
async def test_program_repository_insert(program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    program = await program_repository.get_by_id(program_id)

    assert program_id, 'No id program after data insert'
    assert program, 'Inserted program not found'
    assert isinstance(program_id, int), 'Wrong id program type'


@pytest.mark.asyncio
async def test_program_repository_update(program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    program = await program_repository.get_by_id(program_id)
    OLD_VALUE = program.data.notes
    program.data.notes += 'UPDATED'
    updated_program = await program_repository.update(program)

    assert updated_program, 'Updated program not found'
    assert updated_program.id == program_id, 'Inserted and updated programs\' ids are not same'
    assert updated_program.data.notes == OLD_VALUE + 'UPDATED'


@pytest.mark.asyncio
async def test_program_repository_get_by_id(program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    program = await program_repository.get_by_id(program_id)

    assert program, 'Program not found'
    assert program.id == program_id, 'Wrong program id'
    assert program.data.program_name == program_data.program_name, 'Wrong program name'


@pytest.mark.asyncio
async def test_program_repository_list(program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    programs = await program_repository.list()

    assert programs, 'Programs not found'
    assert isinstance(programs, list), 'Wrong programs type'
    assert len(programs) > 0, 'Wrong programs amount'


@pytest.mark.asyncio
async def test_program_repository_delete(asset_repository, program_repository, program_data):
    program_id = await program_repository.insert(program_data)
    program = await program_repository.get_by_id(program_id)

    await program_repository.delete(program_id)
    deleted_program = await program_repository.get_by_id(program_id)

    assets = await asset_repository.list(program_id)

    assert program_id, 'ProgramData was not inserted'
    assert program, 'Can not find the inserted program'
    assert not deleted_program, 'The program was not deleted'
    assert len(assets) == 0, 'Assets were not deleted'
