from pydantic import BaseModel, Field


class SearchFilter(BaseModel):
    id: str = Field()
