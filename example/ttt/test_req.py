import pytest
from pytest_mock import MockerFixture
import asyncio
from aiohttp import ClientSession, ClientResponse
from unittest.mock import MagicMock, patch, AsyncMock

from req import fetch_data


@pytest.mark.asyncio
async def test_exec(mocker: MockerFixture):
    
    response_mock = mocker.MagicMock(spec_set=ClientResponse)
    response_mock.__aenter__.return_value.json.return_value = {'id': 123}

    session_mock = mocker.MagicMock(spec_set=ClientSession)
    session_mock.get.return_value = response_mock

    # Var 1
    mocker.patch.object(ClientSession, '__aenter__', return_value=session_mock)
    result = await fetch_data('https://dummyjson.com/products/1')

    assert result.id == 123
    
    # Var 2
    # with patch('req.aiohttp.ClientSession') as session_mock_class:
    #     session_mock_class.return_value.__aenter__.return_value = session_mock

    #     result = await fetch_data('https://dummyjson.com/products/1')

    #     assert result.id == 123
