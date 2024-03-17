import pytest

from asman.domains.example.use_cases.example_use_case import ExampleUseCase
from asman.domains.example import Request


@pytest.fixture
def example_use_case(usecase_config, dynamodb_config):
    use_case = ExampleUseCase(usecase_config, dynamodb_config)

    return use_case


def test_example_use_case_create(usecase_config, dynamodb_config):
    use_case = ExampleUseCase(usecase_config, dynamodb_config)

    assert use_case
    assert use_case.repo


def test_example_use_case_execute(example_use_case):
    request = Request(
        data='test'
    )

    response = example_use_case.execute(request)

    assert response == request.data
