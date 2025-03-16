import logging
import requests
import json
from bottle import HTTPError

from whois_service_cURL.models.class_models import ResponseModel, status_domainAvailable, final_info_for_domain
from whois_service_cURL.database.save_to_db import save_to_db

from whois_service_cURL.database.create_table import create_table

create_table()

logging.basicConfig(level=logging.INFO)

ALLOWED_TLDS = {'.kz', '.com.kz', '.org.kz', '.com', '.ru', '.net', '.asia'}

HEADERS = {
    'accept': '*/*',
    'content-type': 'application/json',
    'origin': 'https://www.ps.kz',
    'referer': 'https://www.ps.kz/',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
}

API_URL = "https://console.ps.kz/vitrina/graphql"


def is_valid_domain(domain_name: str) -> bool:
    return domain_name and '.' in domain_name and any(domain_name.endswith(tld) for tld in ALLOWED_TLDS)


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


def validate_whois_data(domain_name: str, all_info_for_domain: dict) -> ResponseModel:
    try:
        return ResponseModel(**all_info_for_domain)
    except Exception as e:
        logging.error(f"Ошибка валидации данных: {e}")
        raise HTTPError(400, f'Информация о домене {domain_name} в ps.kz недостаточна')


def process_whois_data(domain_name: str) -> str:
    all_info_for_domain = fetch_whois_data(domain_name)
    logging.info(f'Получены данные для {domain_name}')

    response_obj = validate_whois_data(domain_name, all_info_for_domain)

    if status_domainAvailable(response_obj):
        logging.warning(f'Домен {domain_name} доступен для регистрации')
        raise HTTPError(400, f'Домен {domain_name} не зарегистрирован и доступен для регистрации')

    whois_data = final_info_for_domain(response_obj)
    if not whois_data:
        logging.error(f'Не удалось извлечь данные WHOIS для {domain_name}')
        raise HTTPError(404, f'Не удалось извлечь данные WHOIS для {domain_name}')

    save_whois_data(domain_name, whois_data)
    return f'Данные для {domain_name} успешно сохранены \n{json.dumps(whois_data, indent=4, ensure_ascii=False)}'


def save_whois_data(domain_name: str, whois_data: dict):
    try:
        logging.info(f'Сохранение данных WHOIS для {domain_name} в БД')
        save_to_db(whois_data)
        logging.info(f'Данные успешно сохранены')
    except Exception as e:
        logging.error(f'Ошибка при сохранении данных WHOIS для {domain_name}: {str(e)}')
        raise HTTPError(500, f'Ошибка при сохранении данных WHOIS: {str(e)}')


def whois_data_check(domain_name: str) -> str:
    logging.info(f'Запрос WHOIS для домена: {domain_name}')
    if not is_valid_domain(domain_name):
        logging.warning(f'Некорректное доменное имя: {domain_name}')
        raise HTTPError(400, f'{domain_name} — некорректный домен')
    return process_whois_data(domain_name)

# domain_name = 'example.kz'
# whois_data_check(domain_name)
