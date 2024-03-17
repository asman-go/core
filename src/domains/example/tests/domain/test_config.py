from asman.domains.example.domain.config import Config


def test_config_init(monkeypatch):
    ENV_SOME_VALUE = 'testtest'

    monkeypatch.setenv('some_value', ENV_SOME_VALUE)

    config = Config()

    assert config
    assert config.value
    assert config.value == ENV_SOME_VALUE
