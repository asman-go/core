import pytest

from asman.tasks.common import HelloTask


def test_hello():
    payload = 'Test'
    assert HelloTask(payload) == f'Hello {payload}'
