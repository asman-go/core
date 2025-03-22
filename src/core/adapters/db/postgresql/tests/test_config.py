from asman.core.adapters.db.postgresql import PostgresConfig


def test_postgres_config_create(monkeypatch):
    POSTGRES_DB = '1'
    POSTGRES_USER = '2'
    POSTGRES_PASSWORD = '3'
    DEFAULT_HOST = 'localhost'
    DEFAULT_PORT = 5432

    monkeypatch.setenv('POSTGRES_DB', POSTGRES_DB)
    monkeypatch.setenv('POSTGRES_USER', POSTGRES_USER)
    monkeypatch.setenv('POSTGRES_PASSWORD', POSTGRES_PASSWORD)
    monkeypatch.setenv('POSTGRES_HOST', DEFAULT_HOST)
    monkeypatch.setenv('POSTGRES_PORT', DEFAULT_PORT)

    config = PostgresConfig()

    assert config
    assert config.POSTGRES_DB == POSTGRES_DB
    assert config.POSTGRES_USER == POSTGRES_USER
    assert config.POSTGRES_PASSWORD == POSTGRES_PASSWORD
    assert config.POSTGRES_HOST == DEFAULT_HOST
    assert config.POSTGRES_PORT == DEFAULT_PORT
