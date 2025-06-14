from typing import Type
import uplink


def parse_response(response_model: Type):
    @uplink.response_handler()
    def _parse_as_pydantic_model(response):
        if response.status_code == 200:
            # TODO: parse response
            # print(dir(response))
            return response
        else:
            # TODO: parse error
            return response

    return _parse_as_pydantic_model
