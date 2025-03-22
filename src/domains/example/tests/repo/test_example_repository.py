from asman.domains.example.repo.example_repository import ExampleRepository
from asman.domains.example.api import SearchFilter


def test_example_repository_create(database):
    repo = ExampleRepository(database)

    assert repo
    assert repo.database


def test_example_repository_crud(example_repository, example_data):
    updated_entities = example_repository.update([example_data])
    assert updated_entities
    assert len(updated_entities) == 1
    assert updated_entities[0].address == example_data.address

    new_entities = example_repository.search([
        SearchFilter(
            id=updated_entities[0].id,
        ),
    ])


    assert new_entities
    assert len(new_entities) == 1
    assert new_entities[0].id == updated_entities[0].id
    assert new_entities[0].address == example_data.address
