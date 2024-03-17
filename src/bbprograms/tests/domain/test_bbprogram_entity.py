import pytest


from bbprograms import (
    AssetEntity,
    BugBountyProgramEntity,

    InvalidPlatformException,
)


def test_bbprogram_create():
    program = BugBountyProgramEntity(
        program_name='Test',
        program_site='https://example.com',
        platform='hackerone',
        in_scope=[
            AssetEntity(
                type='host',
                value='127.0.0.1',
                is_paid=False
            ),
            AssetEntity(
                type='domain',
                value='example.com',
                is_paid=True
            )
        ],
        out_of_scope=[
            AssetEntity(
                type='subnet',
                value='192.168.0.0/24',
                is_paid=False
            )
        ],
        notes='Some notes',
    )

    assert program
    assert program.id
    assert program.program_name == 'Test'
    assert program.program_site == 'https://example.com'
    assert program.platform == 'hackerone'
    assert len(program.in_scope) == 2
    assert len(program.out_of_scope) == 1
    assert program.notes == 'Some notes'


def test_bbprogram_create_throws_invalid_platform_exception():
    with pytest.raises(InvalidPlatformException) as exc:
        BugBountyProgramEntity(
            program_name='Test',
            program_site='https://example.com',
            platform='TOTALLY_NOT_A_PLATFORM',
            in_scope=[],
            out_of_scope=[],
            notes='Some notes',
        )

    assert isinstance(exc.value, InvalidPlatformException)
