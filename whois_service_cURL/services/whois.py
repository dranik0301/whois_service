from bottle import HTTPError
import logging
import requests
import json

from whois_service_cURL.module.class_module import ResponseModel, status_domainAvailable, final_info_for_domain

from whois_service_cURL.database.save_to_db import save_to_db
from whois_service_cURL.database.create_table import create_table

logging.basicConfig(level=logging.INFO)


def take_info_for_domain(domain_name: str) -> json:
    headers = {
        'accept': '*/*',
        'accept-language': 'ru-RU,ru;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.ps.kz',
        'priority': 'u=1, i',
        'referer': 'https://www.ps.kz/',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
    }

    params = {
        'lang': 'ru',
        'opname': 'WhoisResultPageQuery',
    }

    json_data = {
        'operationName': 'WhoisResultPageQuery',
        'variables': {
            'domainName': f'{domain_name}',
        },
        'query': 'query WhoisResultPageQuery($domainName: String!) {\n  vitrina {\n    domains {\n      whois(domainName: $domainName) {\n        ...WhoisResultPageData\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment WhoisResultPageData on WhoisOutputType {\n  status {\n    domainAvailable\n    preorderAvailability\n    remainingDays\n    tariffKey\n    releaseDate\n    asciiName\n    premiumDomain\n    domainPremiumPrice\n    regAvailability\n    __typename\n  }\n  data {\n    domain\n    idn\n    statuses\n    currentRegistrar\n    nameservers\n    createdAt\n    updatedAt\n    expiresAt\n    transferredAt\n    registrant {\n      name\n      organization\n      country\n      city\n      postalCode\n      street\n      phone\n      email\n      __typename\n    }\n    admin {\n      name\n      organization\n      country\n      city\n      postalCode\n      street\n      phone\n      email\n      __typename\n    }\n    __typename\n  }\n  rawData\n  prices {\n    registration\n    __typename\n  }\n  __typename\n}',
    }

    response = requests.post('https://console.ps.kz/vitrina/graphql', params=params, headers=headers, json=json_data)

    json_data = json.loads(response.text)
    pretty_json = json.dumps(json_data, indent=4, ensure_ascii=False)

    # print(1, type(response))  # <class 'requests.models.Response'>
    # print(2, type(json_data))  # <class 'dict'>
    # print(3, type(pretty_json))  # <class 'str'>

    return json_data


def whois_data_check(domain_name: str) -> str:
    logging.info(f'Получен запрос на WHOIS для домена: {domain_name}. Проверяем корректность доменного имени')
    try:
        allowed_tlds = {'.kz', '.com.kz', '.org.kz', '.com', '.ru', '.net', '.asia'}
        if not domain_name or '.' not in domain_name or not any(domain_name.endswith(tld) for tld in allowed_tlds):
            logging.info(f'{domain_name} — некорректный домен')
            raise HTTPError(400, f'{domain_name} — некорректный домен')
        logging.info(f'{domain_name} — корректный домен')

        all_info_for_domain = take_info_for_domain(domain_name)

        response_obj = ResponseModel(**all_info_for_domain)
        if status_domainAvailable(response_obj) is True:
            logging.error(f'Домен {domain_name} не зарегистрирован и доступен для регистрации')
            raise HTTPError(400, f'Домен {domain_name} не зарегистрирован и доступен для регистрации')

        whois_data = final_info_for_domain(response_obj)

        if not whois_data:
            logging.error(f'Не удалось извлечь данные для домена: {domain_name}')
            raise HTTPError(404, f'Не удалось извлечь данные для домена: {domain_name}')

        create_table()

        try:
            logging.info(f'Попытка сохранить данные {domain_name} в БД')
            save_to_db(whois_data)
            logging.info(f'Данные WHOIS для {domain_name} успешно сохранены в БД')
        except Exception as e:
            logging.error(f'Ошибка при сохранении данных WHOIS для {domain_name}')
            raise HTTPError(500, f'Ошибка при сохранении данных WHOIS для {domain_name}: {str(e)}')

        whois_data_str = json.dumps(final_info_for_domain(response_obj), indent=4, ensure_ascii=False)
        return f'Данные с {domain_name} успешно сохранены \n{whois_data_str}'

    except Exception as e:
        logging.error(f'Ошибка при выполнении запроса WHOIS для {domain_name}: {str(e)}')
        raise HTTPError(500, f'Произошла ошибка: {str(e)}')

# domain_name = 'example.com'
# whois_data_check(domain_name)
