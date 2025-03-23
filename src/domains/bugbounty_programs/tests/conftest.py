import pytest

from asman.core.adapters.db import DatabaseFacade, Databases
from asman.domains.bugbounty_programs.domain import (
    TABLE_ASSET_NAME,
    TABLE_BUGBOUNTY_PROGRAM_NAME,
)
from asman.domains.bugbounty_programs.api import (
    Asset,
    AssetType,
    ProgramData,
)
from asman.domains.bugbounty_programs.repo import (
    AssetRepository,
    ProgramRepository,
)
from asman.domains.bugbounty_programs.use_cases import (
    AddAssetsUseCase,
    RemoveAssetsUseCase,
    DeleteProgramUseCase,
    CreateProgramUseCase,
    ReadProgramUseCase,
    ReadProgramByIdUseCase,
    UpdateProgramUseCase,
)

from asman.core.adapters.tests import db_in_memory, postgres, postgres_config
from asman.core.adapters.db.postgresql import Postgres
from asman.core.adapters.db import DatabaseFacade, Databases
from asman.core.adapters.db.postgresql.tests import init_postgres_envs


@pytest.fixture
def postgres_facade(init_postgres_envs) -> DatabaseFacade:
    return DatabaseFacade(Databases.PostgreSQL)

@pytest.fixture
def init_postgres_envs(monkeypatch):
    monkeypatch.setenv('POSTGRES_DB', 'my_db')
    monkeypatch.setenv('POSTGRES_USER', 'my_user')
    monkeypatch.setenv('POSTGRES_PASSWORD', 'my_password')
    monkeypatch.setenv('POSTGRES_HOST', 'localhost')
    monkeypatch.setenv('POSTGRES_PORT', '6432')


@pytest.fixture
def postgres_instance(init_postgres_envs) -> Postgres:
    return Postgres()


@pytest.fixture
def asset_repository(db_in_memory):
    return AssetRepository(db_in_memory)


@pytest.fixture
def program_repository(db_in_memory):
    return ProgramRepository(db_in_memory)


@pytest.fixture
def assets():
    return [
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
    ]


@pytest.fixture
def program_data(assets):
    return ProgramData(
        program_name='NewProgram',
        program_site='https://example.com/program',
        platform='h1',
        assets=assets,
        notes='Some notes'
    )


@pytest.fixture
def program_data_other(assets):
    return ProgramData(
        program_name='NewProgram',
        program_site='https://example.com/program1',
        platform='h1',
        assets=assets,
        notes='Some notes'
    )


@pytest.fixture
def add_assets_use_case(postgres_config):
    return AddAssetsUseCase(None, postgres_config)


@pytest.fixture
def remove_assets_use_case(postgres_config):
    return RemoveAssetsUseCase(None, postgres_config)


@pytest.fixture
def create_program_use_case(postgres_config):
    return CreateProgramUseCase(None, postgres_config)


@pytest.fixture
def delete_program_use_case(postgres_config):
    return DeleteProgramUseCase(None, postgres_config)


@pytest.fixture
def read_program_use_case(postgres_config):
    return ReadProgramUseCase(None, postgres_config)


@pytest.fixture
def read_program_by_id_use_case(postgres_config):
    return ReadProgramByIdUseCase(None, postgres_config)


@pytest.fixture
def update_program_use_case(postgres_config):
    return UpdateProgramUseCase(None, postgres_config)
