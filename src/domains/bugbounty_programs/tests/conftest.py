import pytest

from asman.domains.bugbounty_programs.api import (
    Asset,
    AssetType,
    CreateProgramRequest,
)
from asman.domains.bugbounty_programs.repo import ProgramRepository

from asman.core.adapters.tests import db_in_memory, postgres, postgres_config


@pytest.fixture
def program_repository(db_in_memory):
    return ProgramRepository(db_in_memory)


@pytest.fixture
def create_program_request():
    return CreateProgramRequest(
        program_name='NewProgram',
        program_site='https://example.com/program',
        platform='h1',
        assets=[
            Asset(
                value='example.com',
                type=AssetType.ASSET_WEB,
                in_scope=True,
                is_paid=False,
            ),
            Asset(
                value='192.168.0.1',
                type=AssetType.ASSET_IP,
                in_scope=True,
                is_paid=True,
            ),
            Asset(
                value='https://api.example.com/',
                type=AssetType.ASSET_API,
                in_scope=False,
                is_paid=False,
            ),
        ],
        notes='Some notes'
    )
