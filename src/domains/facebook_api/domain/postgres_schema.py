from asman.core.adapters.db import TableBase
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.schema import PrimaryKeyConstraint

TABLE_DOMAINS_NAME = 'ctdomains'


class TableDomain(TableBase):
    __tablename__ = TABLE_DOMAINS_NAME

    domain = Column(String, primary_key=True)
    parent_domain = Column(String, primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint('domain', 'parent_domain'),
    )
