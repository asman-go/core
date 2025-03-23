import pytest

from asman.domains.bugbounty_programs.repo import ProgramRepository
from asman.domains.bugbounty_programs.api import SearchByID
from asman.domains.bugbounty_programs.domain import TableProgram


def test_program_repository_instance_create(database, program_table_name):
    repo = ProgramRepository(database, program_table_name)

    assert repo, 'No repo in ProgramRepository'
    assert repo.database
    assert repo.table_name == program_table_name


@pytest.mark.asyncio
async def test_program_repository_crud(program_repository, new_program, new_program_other):
    # Проверяем добавление программы
    ids = await program_repository.insert([new_program])

    assert ids and len(ids) == 1

    # Проверяем поиск по фильтру
    search_filter = [
        SearchByID(id=ids[0].program_id),
    ]
    programs = await program_repository.search(search_filter)

    assert programs and len(programs) == 1
    inserted_program = programs[0]
    assert inserted_program == new_program

    # Проверяем, что при добавлении той же программы, поле будет обновлено у уже существующей
    _new_program = new_program.model_copy(
        update={'notes': 'NEW_VALUE'},
        deep=True,
    )
    ids = await program_repository.insert([_new_program])

    assert ids[0].program_id == inserted_program.id

    programs = await program_repository.search(search_filter)

    assert programs[0].notes == 'NEW_VALUE'
    assert programs[0].notes != new_program.notes

    # Обновляем данные, но через update
    ids = await program_repository.update([inserted_program])
    assert ids[0].program_id == inserted_program.id
    programs = await program_repository.search(search_filter)
    assert programs[0].notes == new_program.notes

    # Проверяем, что можем получить все объекты
    await program_repository.insert([new_program_other])
    programs = await program_repository.list()
    assert programs and len(programs) == 2

    # Проверяем удаление объектов
    ids = await program_repository.delete(search_filter)
    assert ids and len(ids) == 1
    assert ids[0].program_id == search_filter[0].id
