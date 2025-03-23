import pytest

from asman.domains.example import ExampleUseCase, Request


@pytest.fixture
def example_use_case(usecase_config, init_dynamodb_envs):
    use_case = ExampleUseCase(usecase_config)

    return use_case


def test_example_use_case_create(usecase_config, init_dynamodb_envs):
    use_case = ExampleUseCase(usecase_config)

    assert use_case
    assert use_case.repo


def test_example_use_case_execute(example_use_case, init_dynamodb_envs):
    request = Request(
        data='test'
    )

    response = example_use_case.execute(request)

    assert response.data == request.data
