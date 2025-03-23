from asman.core.adapters.db.postgresql import TableBase
from sqlalchemy import Column, String
from sqlalchemy.schema import PrimaryKeyConstraint
from asman.domains.services.api import Domain


TABLE_DOMAINS_NAME = 'ctdomains'


class TableDomain(TableBase):
    __tablename__ = TABLE_DOMAINS_NAME

    domain = Column(String, primary_key=True)
    parent_domain = Column(String, primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint('domain', 'parent_domain'),
        {'extend_existing': True},
    )

    @staticmethod
    def convert(item: 'TableDomain') -> Domain:
        return Domain(
            domain=item.domain,
            parent_domain=item.parent_domain,
        )
