import logging
import json
import requests
import sqlite3
from bottle import run, Bottle, response, HTTPError
from pydantic import BaseModel
from typing import List, Optional

logging.basicConfig(level=logging.INFO)

ALLOWED_TLDS = {'.kz', '.com.kz', '.org.kz', '.com', '.ru', '.net', '.asia'}
HEADERS = {
    'accept': '*/*',
    'content-type': 'application/json',
    'origin': 'https://www.ps.kz',
    'referer': 'https://www.ps.kz/',
    'user-agent': 'Mozilla/5.0'
}
API_URL = "https://console.ps.kz/vitrina/graphql"
DB_PATH = "whois.db"


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
    domain: Optional[str]
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
    status: dict
    data: WhoisData


class ResponseModel(BaseModel):
    data: dict


class WhoisDatabase:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS whois_data (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    domain_name TEXT NOT NULL,
                    status TEXT,
                    registrator TEXT,
                    registrant TEXT,
                    admin TEXT,
                    nameservers TEXT,
                    created TEXT,
                    updated TEXT,
                    expires TEXT,
                    transferred TEXT,
                    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                )
            ''')
            logging.info("Таблица whois_data готова к использованию.")

    def save(self, domain_name, whois_data: dict):
        with self.conn:
            self.conn.execute('''
                INSERT INTO whois_data (domain_name, status, registrator, registrant, admin, nameservers, created, updated, expires, transferred)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                domain_name,
                json.dumps(whois_data.get('statuses', [])),
                whois_data.get('currentRegistrar', ''),
                json.dumps(whois_data.get('registrant', {})),
                json.dumps(whois_data.get('admin', {})),
                json.dumps(whois_data.get('nameservers', [])),
                whois_data.get('createdAt', ''),
                whois_data.get('updatedAt', ''),
                whois_data.get('expiresAt', ''),
                whois_data.get('transferredAt', '')
            ))
            logging.info(f'Данные WHOIS для {domain_name} сохранены.')


class WhoisService:
    def __init__(self):
        self.db = WhoisDatabase()

    def is_valid_domain(self, domain_name: str) -> bool:
        return domain_name and any(domain_name.endswith(tld) for tld in ALLOWED_TLDS)

    def fetch_whois_data(self, domain_name: str) -> dict:
        json_data = {
            'operationName': 'WhoisResultPageQuery',
            'variables': {'domainName': domain_name},
            'query': 'query WhoisResultPageQuery($domainName: String!) {\n  vitrina {\n    domains {\n      whois(domainName: $domainName) {\n        ...WhoisResultPageData\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WhoisResultPageData on WhoisOutputType {\n  status {\n    domainAvailable\n    preorderAvailability\n    remainingDays\n    tariffKey\n    releaseDate\n    asciiName\n    premiumDomain\n    domainPremiumPrice\n    regAvailability\n    __typename\n  }\n  data {\n    domain\n    idn\n    statuses\n    currentRegistrar\n    nameservers\n    createdAt\n    updatedAt\n    expiresAt\n    transferredAt\n    registrant {\n      name\n      organization\n      country\n      city\n      postalCode\n      street\n      phone\n      email\n      __typename\n    }\n    admin {\n      name\n      organization\n      country\n      city\n      postalCode\n      street\n      phone\n      email\n      __typename\n    }\n    __typename\n  }\n  rawData\n  prices {\n    registration\n    __typename\n  }\n  __typename\n}',
        }
        try:
            response = requests.post(API_URL, headers=HEADERS, json=json_data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f'Ошибка сети при запросе WHOIS: {str(e)}')
            raise HTTPError(500, f'Ошибка сети: {str(e)}')

    def process_whois_data(self, domain_name: str) -> str:
        all_info_for_domain = self.fetch_whois_data(domain_name)
        response_obj = ResponseModel(**all_info_for_domain)
        whois_data = response_obj.data.get('vitrina', {}).get('domains', {}).get('whois', {}).get('data', {})
        if not whois_data:
            raise HTTPError(404, 'Данные WHOIS не найдены')
        self.db.save(domain_name, whois_data)
        return json.dumps(whois_data, indent=4, ensure_ascii=False)


app = Bottle()
whois_service = WhoisService()


@app.route('/lookup_whois/<domain_name>')
def lookup(domain_name):
    if not whois_service.is_valid_domain(domain_name):
        logging.warning(f'Некорректное доменное имя: {domain_name}')
        raise HTTPError(400, 'Некорректное доменное имя')
    response.content_type = 'application/json'
    return whois_service.process_whois_data(domain_name)


if __name__ == '__main__':
    run(app, host='localhost', port=8080)
