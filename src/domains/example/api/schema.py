from pydantic import BaseModel


class Request(BaseModel):
    data: str


class Response(Request):...
