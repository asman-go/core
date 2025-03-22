from sqlalchemy import (
    Column,
    String,
    Boolean,
    Integer,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from asman.core.adapters.db.postgresql import TableBase

from asman.domains.bugbounty_programs.api import (
    Asset,
    AssetType,
    Program,
    ProgramData,
)

TABLE_ASSET_NAME = 'assets'
TABLE_BUGBOUNTY_PROGRAM_NAME = 'programs'


class TableProgram(TableBase):
    __tablename__ = TABLE_BUGBOUNTY_PROGRAM_NAME

    id = Column(Integer, primary_key=True)
    program_name = Column(String)
    program_site = Column(String)
    platform = Column(String)
    notes = Column(String)

    assets = relationship(
        'TableAsset',   # TableAsset — of python type associated with 'assets' table
        back_populates='program',  # program — field in TableAsset
    )

    __table_args__ = (
        UniqueConstraint('program_site', name=f'uq_{TABLE_BUGBOUNTY_PROGRAM_NAME}_program_site'),
        {'extend_existing': True}
    )

    @staticmethod
    def convert(item: 'TableProgram') -> Program:
        assets = list(
            map(
                lambda asset: TableAsset.convert(asset),
                item.assets
            )
        )

        return Program(
            id=item.id,
            data=ProgramData(
                program_name=item.program_name,
                program_site=item.program_site,
                platform=item.platform,
                assets=assets,
                notes=item.notes,
            ),
        )


class TableAsset(TableBase):
    __tablename__ = TABLE_ASSET_NAME

    id = Column(Integer, primary_key=True)
    value = Column(String)
    # program_id = Column(ForeignKey(f'{TABLE_BUGBOUNTY_PROGRAM_NAME}.id'))
    program_id = Column(ForeignKey(TableProgram.id))

    type = Column(Integer)
    in_scope = Column(Boolean)
    is_paid = Column(Boolean)

    program = relationship(
        TableProgram,
        back_populates='assets',
    )

    __table_args__ = (
        UniqueConstraint('value', 'type', 'program_id', name=f'uq_{TABLE_ASSET_NAME}_value_type'),
        {'extend_existing': True}
    )

    @staticmethod
    def convert(item: 'TableAsset') -> Asset:
        return Asset(
            value=item.value,
            type=AssetType(item.type),
            in_scope=item.in_scope,
            is_paid=item.is_paid,
        )
