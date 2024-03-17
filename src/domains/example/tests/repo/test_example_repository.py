from domains.example.repo.example_repository import ExampleRepository


def test_example_repository_create(dynamodb, dynamodb_table_name):
    repo = ExampleRepository(dynamodb, dynamodb_table_name)

    assert repo
    assert repo.database


def test_example_repository_update(example_repository, example_entity):
    updated_entity = example_repository.update(example_entity)
    new_entity = example_repository.get_by_id({
        'id': {
            'S': example_entity.id
        }
    })

    assert updated_entity
    assert updated_entity.id == example_entity.id
    assert updated_entity.address == example_entity.address

    assert new_entity
    assert new_entity.id == example_entity.id
    assert new_entity.address == example_entity.address
