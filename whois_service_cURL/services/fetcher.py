import requests
import logging
from bottle import HTTPError

from models.class_models import ResponseModel

import os
from dotenv import load_dotenv

load_dotenv()

HEADERS = {
    'accept': os.getenv("HEADERS_ACCEPT"),
    'content-type': os.getenv("HEADERS_CONTENT_TYPE"),
    'origin': os.getenv("HEADERS_ORIGIN"),
    'referer': os.getenv("HEADERS_REFERER"),
    'user-agent': os.getenv("HEADERS_USER_AGENT"),
}

API_URL = os.getenv("API_URL")


class WhoisFetcher:
    @staticmethod
    def fetch_whois_data(domain_name: str) -> dict:
        json_data = {
            'operationName': 'WhoisResultPageQuery',
            'variables': {'domainName': domain_name},
            'query': 'query WhoisResultPageQuery($domainName: String!) {\n  vitrina {\n    domains {\n      whois(domainName: $domainName) {\n        ...WhoisResultPageData\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WhoisResultPageData on WhoisOutputType {\n  status {\n    domainAvailable\n    preorderAvailability\n    remainingDays\n    tariffKey\n    releaseDate\n    asciiName\n    premiumDomain\n    domainPremiumPrice\n    regAvailability\n    __typename\n  }\n  data {\n    domain\n    idn\n    statuses\n    currentRegistrar\n    nameservers\n    createdAt\n    updatedAt\n    expiresAt\n    transferredAt\n    registrant {\n      name\n      organization\n      country\n      city\n      postalCode\n      street\n      phone\n      email\n      __typename\n    }\n    admin {\n      name\n      organization\n      country\n      city\n      postalCode\n      street\n      phone\n      email\n      __typename\n    }\n    __typename\n  }\n  rawData\n  prices {\n    registration\n    __typename\n  }\n  __typename\n}',
        }

        try:
            response = requests.post(API_URL, headers=HEADERS, json=json_data)
            response.raise_for_status()
            logging.info(f'Успешный запрос WHOIS для {domain_name}')
            return response.json()

        except requests.RequestException as e:
            logging.error(f'Ошибка сети при запросе WHOIS для {domain_name}: {str(e)}')
            raise HTTPError(500, f'Ошибка сети: {str(e)}')

        # print(1, type(response))  # <class 'requests.models.Response'>
        # print(2, type(json_data))  # <class 'dict'>

    @staticmethod
    def validate_whois_data(domain_name: str, all_info_for_domain: dict) -> ResponseModel:
        try:
            return ResponseModel(**all_info_for_domain)
        except Exception as e:
            logging.error(f"Ошибка валидации данных: {e}")
            raise HTTPError(400, f'Информация о домене {domain_name} в ps.kz недостаточна')
