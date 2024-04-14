from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from asman.core.adapters.db import TableBase


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
        "TableAsset",   # TableAsset — of python type associated with 'assets' table
        back_populates="program",  # program — field in TableAsset
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
        back_populates="assets",
    )
