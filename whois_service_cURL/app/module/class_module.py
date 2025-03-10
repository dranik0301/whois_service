from pydantic import BaseModel
from typing import List, Optional


class Registrant(BaseModel):
    domainAvailable: Optional[bool]


class WhoisContactInfo(BaseModel):
    name: Optional[str]
    organization: Optional[str]
    country: Optional[str]
    city: Optional[str]
    postalCode: Optional[str]
    street: Optional[str]
    phone: Optional[str]
    email: Optional[str]


class WhoisData(BaseModel):
    domain: str
    statuses: Optional[List[str]]
    currentRegistrar: Optional[str]
    registrant: Optional[WhoisContactInfo]
    admin: Optional[WhoisContactInfo]
    nameservers: Optional[List[str]]
    createdAt: Optional[str]
    updatedAt: Optional[str]
    expiresAt: Optional[str]
    transferredAt: Optional[str]


class Whois(BaseModel):
    status: Registrant
    data: WhoisData


class Domains(BaseModel):
    whois: Whois


class Vitrina(BaseModel):
    domains: Domains


class DataModel(BaseModel):
    vitrina: Vitrina


class ResponseModel(BaseModel):
    data: DataModel


def status_domainAvailable(response_obj) -> bool:
    return bool(response_obj.data.vitrina.domains.whois.status.domainAvailable)


def final_info_for_domain(response_obj) -> dict[str, any]:
    return response_obj.data.vitrina.domains.whois.data.model_dump()
