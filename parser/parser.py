import logging
from typing import List, Dict
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)

def parse_contact_info(contact_info: List) -> Dict[str, str]:
    data = {}
    for subheadings in contact_info:
        subheading = subheadings.find_all("li")
        if len(subheading) < 2:
            logging.warning("Unexpected format in contact info: missing key-value pair")
            continue
        key = subheading[0].get_text(strip=True)
        value = subheading[1].get_text(strip=True)
        data[key] = value
    return data

def get_whois_data(soup: BeautifulSoup) -> Dict[str, any]:
    data = {}

    rows = soup.find(class_="font-size-24")
    if rows and rows.get_text(strip=True):      #Проверяем, есть ли текст внутри
        logging.error("WHOIS information does not exist for the given link")
        raise SystemExit("WHOIS information does not exist for the given link")     #нету никакой информации по ссылки

    rows = soup.find_all(class_="whois-result-table__row")
    for row in rows:
        title = row.find(class_="whois-result-table__title")

        if title:
            text = title.get_text(strip=True)
            logging.info(f"Parsing section: {text}")

            if text == 'Доменное имя:':
                domen_info = row.find(class_="font-weight-bold")
                data['domen_info'] = domen_info.get_text(strip=True) if domen_info else "Not found"

            elif text == 'Статус:':
                data_status = {}
                status_info = row.find_all("ul")
                for item in status_info:
                    status_info_li = item.find_all("li")
                    if len(status_info_li) < 2:
                        logging.warning(f"Unexpected format in status section: {status_info_li}")
                        continue
                    key = status_info_li[0].get_text(strip=True)
                    value = status_info_li[1].get_text(strip=True)
                    data_status[key] = value
                data['status'] = data_status

            elif text == 'Регистратор:':
                registrar = row.find(class_="font-weight-bold")
                data['registrar'] = registrar.get_text(strip=True) if registrar else "Not found"

            elif text == 'Регистрант:':
                registrant = row.find_all("ul")
                data['registrant'] = parse_contact_info(registrant)

            elif text == 'Административный контакт:':
                administrative_contact = row.find_all("ul")
                data['administrative_contact'] = parse_contact_info(administrative_contact)

            elif text == 'Сервера имен:':
                buf_list = []
                servers_name = row.find_all(class_="font-weight-bold")
                for server_name in servers_name:
                    buf_list.append(server_name.get_text(strip=True))
                data['server_name'] = buf_list

            elif text == 'Создан:':
                created = row.find(class_="whois-result-table__description")
                data['created'] = created.get_text(strip=True) if created else "Not found"

            elif text == 'Дата окончания:':
                expiration_date = row.find(class_="font-weight-bold")
                data['expiration_date'] = expiration_date.get_text(strip=True) if expiration_date else "Not found"

            elif text == 'Дата трансфера:':
                transfer_date = row.find(class_="whois-result-table__description")
                data['transfer_date'] = transfer_date.get_text(strip=True) if transfer_date else "Not found"

    logging.info("WHOIS data successfully parsed")
    return data
