from asman.domains.example import (
    ExampleUseCase,
    Request,
)

from asman.core.adapters.db import DynamoDBConfig

if __name__ == '__main__':
    config = DynamoDBConfig()
    use_case = ExampleUseCase(None, config)
    request = Request(data='test1')
    print(use_case.execute(request))
