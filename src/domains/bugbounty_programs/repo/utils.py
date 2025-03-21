from pydantic import BaseModel, Field


class SearchById(BaseModel):
    id: str = Field()


class SearchByProgramId(BaseModel):
    program_id: int = Field()
