from pydantic import BaseModel, Field
from typing import List, Optional


class Cursor(BaseModel):
    after: str = ""
    before: str = ""


class Paginator(BaseModel):
    cursors: Cursor
    next: str = ""


class CertificateInfo(BaseModel):
    cert_hash_sha256: str
    domains: List[str]
    issuer_name: str
    subject_name: str
    id: str


class FacebookCertificateResponse(BaseModel):
    data: List[CertificateInfo] = Field(default_factory=lambda: [])
    paging: Paginator | None = Field(default=None)
