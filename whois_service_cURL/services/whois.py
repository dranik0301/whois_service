import logging
import json
from bottle import HTTPError

from services.fetcher import WhoisFetcher
from models.class_models import status_domainAvailable, final_info_for_domain

from database.data_and_table import WhoisDatabase

logging.basicConfig(level=logging.INFO)

ALLOWED_TLDS = {'.kz', '.com.kz', '.org.kz', '.com', '.ru', '.net', '.asia'}


class WhoisService:

    def __init__(self):
        self.fetcher = WhoisFetcher()
        self.database = WhoisDatabase()

    def save_whois_data(self, domain_name: str, whois_data: dict):
        try:
            logging.info(f'Сохранение данных WHOIS для {domain_name} в БД')
            self.database.save_to_db(whois_data)
            logging.info(f'Данные успешно сохранены')
        except Exception as e:
            logging.error(f'Ошибка при сохранении данных WHOIS для {domain_name}: {str(e)}')
            raise HTTPError(500, f'Ошибка при сохранении данных WHOIS: {str(e)}')

    @staticmethod
    def is_valid_domain(domain_name: str) -> bool:
        return domain_name and '.' in domain_name and any(domain_name.endswith(tld) for tld in ALLOWED_TLDS)

    def process_whois_data(self, domain_name: str) -> str:
        all_info_for_domain = self.fetcher.fetch_whois_data(domain_name)
        logging.info(f'Получены данные для {domain_name}')

        response_obj = self.fetcher.validate_whois_data(domain_name, all_info_for_domain)

        if status_domainAvailable(response_obj):
            logging.warning(f'Домен {domain_name} доступен для регистрации')
            raise HTTPError(400, f'Домен {domain_name} не зарегистрирован и доступен для регистрации')

        whois_data = final_info_for_domain(response_obj)
        if not whois_data:
            logging.error(f'Не удалось извлечь данные WHOIS для {domain_name}')
            raise HTTPError(404, f'Не удалось извлечь данные WHOIS для {domain_name}')

        self.save_whois_data(domain_name, whois_data)
        return f'Данные для {domain_name} успешно сохранены \n\n{json.dumps(whois_data, indent=4, ensure_ascii=False)}'

    def whois_data_check(self, domain_name: str) -> str:
        logging.info(f'Запрос WHOIS для домена: {domain_name}')
        if not self.is_valid_domain(domain_name):
            logging.warning(f'Некорректное доменное имя: {domain_name}')
            raise HTTPError(400, f'{domain_name} — некорректное доменное имя')
        return self.process_whois_data(domain_name)

# abj = WhoisService()
# domain_name = 'example.kz'
# abj.whois_data_check(domain_name)
