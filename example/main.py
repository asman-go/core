import os

from asman.domains.example import (
    ExampleUseCase,
    Request,
)


if __name__ == '__main__':
    os.environ['DOCUMENT_API_ENDPOINT'] = 'http://localhost:8000'
    os.environ['AWS_ACCESS_KEY_ID'] = '12345'
    os.environ['some_value'] = '123456'

    use_case = ExampleUseCase()
    request = Request(data='test1')
    print(use_case.execute(request))
