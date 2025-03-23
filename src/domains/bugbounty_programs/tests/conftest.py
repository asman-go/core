import pytest
from typing import Sequence

from asman.core.adapters.db import DatabaseFacade, Databases
from asman.domains.bugbounty_programs.domain import (
    TABLE_ASSET_NAME,
    TABLE_BUGBOUNTY_PROGRAM_NAME,
)
from asman.domains.bugbounty_programs.api import (
    Asset,
    AssetType,
    NewProgram,
    NewAsset,
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

from asman.core.adapters.db import DatabaseFacade, Databases
from asman.core.adapters.db.tests import postgres_facade
from asman.core.adapters.db.postgresql.tests import init_postgres_envs


@pytest.fixture
def database(postgres_facade) -> DatabaseFacade:
    return postgres_facade


@pytest.fixture
def program_table_name() -> str:
    return TABLE_BUGBOUNTY_PROGRAM_NAME


@pytest.fixture
def asset_table_name() -> str:
    return TABLE_ASSET_NAME


@pytest.fixture
def asset_repository(database, asset_table_name):
    return AssetRepository(database, asset_table_name)


@pytest.fixture
def program_repository(database, program_table_name):
    return ProgramRepository(database, program_table_name)


@pytest.fixture
def new_assets() -> Sequence[NewAsset]:
    return [
        NewAsset(
            value='example.com',
            type=AssetType.ASSET_WEB,
            in_scope=True,
            is_paid=False,
        ),
        NewAsset(
            value='192.168.0.1',
            type=AssetType.ASSET_IP,
            in_scope=True,
            is_paid=True,
        ),
        NewAsset(
            value='https://api.example.com/',
            type=AssetType.ASSET_API,
            in_scope=False,
            is_paid=False,
        ),
    ]


@pytest.fixture
def new_program() -> NewProgram:
    return NewProgram(
        program_name='NewProgram',
        program_site='https://example.com/program',
        platform='h1',
        notes='Some notes'
    )


@pytest.fixture
def new_program_other() -> NewProgram:
    return NewProgram(
        program_name='NewProgram',
        program_site='https://example.com/program1',
        platform='h1',
        notes='Some notes'
    )


@pytest.fixture
def add_assets_use_case(init_postgres_envs):
    return AddAssetsUseCase()


@pytest.fixture
def remove_assets_use_case(init_postgres_envs):
    return RemoveAssetsUseCase()


@pytest.fixture
def create_program_use_case(init_postgres_envs):
    return CreateProgramUseCase()


@pytest.fixture
def delete_program_use_case(init_postgres_envs):
    return DeleteProgramUseCase()


@pytest.fixture
def read_program_use_case(init_postgres_envs):
    return ReadProgramUseCase()


@pytest.fixture
def read_program_by_id_use_case(init_postgres_envs):
    return ReadProgramByIdUseCase()


@pytest.fixture
def update_program_use_case(init_postgres_envs):
    return UpdateProgramUseCase()
