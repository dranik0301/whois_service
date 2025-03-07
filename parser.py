import logging
from typing import List, Dict
from bs4 import BeautifulSoup

from working_with_database.create_table import create_table
from class_module import WhoIsModel

logging.basicConfig(level=logging.INFO)

create_table()


def extract_description(row: BeautifulSoup) -> str:
    description = row.find(class_="whois-result-table__description")
    return description.get_text(strip=True) if description else None


def parse_information_subtitle(information_subtitle: List) -> Dict[str, str]:
    data = {}
    for subheadings in information_subtitle:
        subheading = subheadings.find_all("li")
        if len(subheading) < 2:
            logging.warning("Неожиданный формат в контактной информации: отсутствует ключ-значение")
            continue
        key = subheading[0].get_text(strip=True)
        value = subheading[1].get_text(strip=True)
        data[key] = value
    return data


def get_whois_data(domain_name: str, soup: BeautifulSoup) -> WhoIsModel:
    data = {}
    mapping = {
        'Доменное имя:': ('domain_name', extract_description),
        'Статус:': ('status', parse_information_subtitle),
        'Регистратор:': ('registrar', extract_description),
        'Регистрант:': ('registrant', parse_information_subtitle),
        'Административный контакт:': ('administrative_contact', parse_information_subtitle),
        'Сервера имен:': (
            'server_name', lambda row: [s.get_text(strip=True) for s in row.find_all(class_="font-weight-bold")]),
        'Создан:': ('created', extract_description),
        'Последнее изменение:': ('last_modified', extract_description),
        'Дата окончания:': ('expiration_date', extract_description),
        'Дата трансфера:': ('transfer_date', extract_description)
    }

    for row in soup.find_all(class_="whois-result-table__row"):
        title = row.find(class_="whois-result-table__title")
        if not title:
            continue

        text = title.get_text(strip=True)
        logging.info(f"Анализируем раздел: {text.strip(":")}")

        if text in mapping:
            key, func = mapping[text]
            value = func(row.find_all("ul")) if func == parse_information_subtitle else func(row)
            data[key] = value
            logging.info(f"Данные для {key} извлечены")

    if not data:
        return {}

    logging.info("Данные WHOIS успешно обработаны")

    whois_obj = WhoIsModel(
        domain_name=data.get("domain_name", ""),
        status=data.get("status", {}),
        registrator=data.get("registrator", ""),
        registrant=data.get("registrant", {}),
        administrative_contact=data.get("administrative_contact", {}),
        server_name=data.get("server_name", []),
        created=data.get("created", ""),
        last_modified=data.get("last_modified", ""),
        expiration_date=data.get("expiration_date", ""),
        transfer_date=data.get("transfer_date", "")
    )

    return whois_obj
