import json
from typing import List, Dict


class WhoIsModel:

    def __init__(
            self,
            domain_name: str,
            status: Dict[str, str],
            registrator: str,
            registrant: Dict[str, str],
            administrative_contact: Dict[str, str],
            server_name: List[str],
            created: str,
            last_modified: str,
            expiration_date: str,
            transfer_date: str
    ):
        self.domain_name = domain_name
        self.status = status
        self.registrator = registrator
        self.registrant = registrant
        self.administrative_contact = administrative_contact
        self.server_name = server_name
        self.created = created
        self.last_modified = last_modified
        self.expiration_date = expiration_date
        self.transfer_date = transfer_date

    def to_dict(self):
        return {
            "domain_name": self.domain_name,
            "status": self.status,
            "registrator": self.registrator,
            "registrant": self.registrant,
            "administrative_contact": self.administrative_contact,
            "server_name": self.server_name,
            "created": self.created,
            "last_modified": self.last_modified,
            "expiration_date": self.expiration_date,
            "transfer_date": self.transfer_date
        }

    def __str__(self):
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)
