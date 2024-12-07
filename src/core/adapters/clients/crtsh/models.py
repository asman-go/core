import pydantic
import typing


class CertificateInfo(pydantic.BaseModel):
    issuer_ca_id: int
    issuer_name: str
    common_name: str
    name_value: str
    id: int
    entry_timestamp: typing.Optional[str]
    not_before: str
    not_after: str
    serial_number: str
    result_count: int
