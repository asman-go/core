import pydantic
import sqlalchemy
from sqlalchemy.orm import relationship

from asman.core.adapters.db.postgresql import TableBase


TABLE_DEBUG_NAME = 'table_debug'
TABLE_CHILDREN_NAME = 'children'
TABLE_PARENTS_NAME = 'parents'
TABLE_PARENT_CHILD_ASSOCIATION_NAME = f'{TABLE_PARENTS_NAME}_{TABLE_CHILDREN_NAME}'


class TableParent(TableBase):
    __tablename__ = TABLE_PARENTS_NAME

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    address = sqlalchemy.Column(sqlalchemy.String)

    children = relationship(
        'TableChild',  # TableChild — of python type associated with 'children' table
        secondary=TABLE_PARENT_CHILD_ASSOCIATION_NAME,  # Для many-to-many связи
        back_populates='parents',   # parents — field in TableAsset
    )

    __table_args__ = (
        # под каждую уникальную колонку надо constraint заводить со своим именем?
        sqlalchemy.UniqueConstraint('name', name=f'uq_{TABLE_PARENTS_NAME}_name'),
        {'extend_existing': True}
    )


class TableChild(TableBase):
    __tablename__ = TABLE_CHILDREN_NAME

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String)

    parents = relationship(
        TableParent,
        secondary=TABLE_PARENT_CHILD_ASSOCIATION_NAME,  # Для many-to-many связи
        back_populates='children',
    )

    __table_args__ = {
        'extend_existing': True
    }


class TableParentChildAssociation(TableBase):
    __tablename__ = TABLE_PARENT_CHILD_ASSOCIATION_NAME

    # parent_name = sqlalchemy.Column(sqlalchemy.String)
    parent_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(f'{TABLE_PARENTS_NAME}.id'),
        primary_key=True,
    )

    child_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(f'{TABLE_CHILDREN_NAME}.id'),
        primary_key=True,
    )

    __table_args__ = (
        # sqlalchemy.ForeignKeyConstraint(
        #     ['parent_id', 'parent_name'],
        #     [f'{TABLE_PARENTS_NAME}.id', f'{TABLE_PARENTS_NAME}.name'],
        # ),
        {'extend_existing': True},
    )


class TableDebug(TableBase):
    __tablename__ = TABLE_DEBUG_NAME

    item = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    name = sqlalchemy.Column(sqlalchemy.String, primary_key=True)
    debug = sqlalchemy.Column(sqlalchemy.Boolean)

    __table_args__ = (
        sqlalchemy.PrimaryKeyConstraint('item', 'name'),
        {'extend_existing': True},
    )

    @staticmethod
    def convert(obj: 'TableDebug') -> 'Item':
        return Item(
            item=obj.item,
            name=obj.name,
            debug=obj.debug,
        )


class Child(pydantic.BaseModel):
    name: str


class Parent(pydantic.BaseModel):
    name: str
    address: str

    def __eq__(self, value):
        return isinstance(value, Parent) and self.name == value.name

    def __hash__(self):
        return hash(str({'name': self.name}))


class Item(pydantic.BaseModel):
    model_config = {"frozen": True}
    item: str = pydantic.Field()
    name: str = pydantic.Field()
    debug: bool = pydantic.Field(default=False)

    def __eq__(self, value):
        return isinstance(value, Item) and self.item == value.item and self.name == value.name

    def __hash__(self):
        return hash(str(
            {
                "item": self.item,
                "name": self.name,
            }
        ))
