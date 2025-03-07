from bs4 import BeautifulSoup
from bottle import HTTPError
import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser import get_whois_data
from working_with_database.save_to_db import save_to_db


def whois_data_check(domain_name: str) -> str:
    driver = None

    try:
        allowed_tlds = {".kz", ".com.kz", ".org.kz", ".com", ".ru", ".net", ".asia"}
        if not domain_name or "." not in domain_name or not any(domain_name.endswith(tld) for tld in allowed_tlds):
            logging.info(f"{domain_name} — некорректный домен")
            raise HTTPError(400, f'{domain_name} — некорректный домен')

        logging.info(f"{domain_name} — корректный домен")

        driver = webdriver.Firefox()
        url = f"https://www.ps.kz/domains/whois/result?q={domain_name}"
        driver.get(url)

        time.sleep(5)

        try:
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "whois-result"))
            )
            logging.info("Таблица найдена")
        except:
            logging.info("Таблица не найдена")
            driver.quit()

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        if soup.find(class_="whois-result-block whois-result-block__vacant"):
            logging.error(f"Домен {domain_name} не зарегистрирован и доступен для регистрации")
            raise HTTPError(400, f'{domain_name} — некорректный домен')

        whois_data = get_whois_data(domain_name, soup)

        if not whois_data:
            logging.error(f"Не удалось извлечь данные для домена: {domain_name}")
            raise HTTPError(404, f"Не удалось извлечь данные для домена: {domain_name}")

        try:
            logging.info(f"Попытка сохранить данные {domain_name} в БД")
            save_to_db(whois_data)
            logging.info(f"Данные WHOIS для {domain_name} успешно сохранены в БД")
        except Exception as e:
            logging.error(f"Ошибка при сохранении данных WHOIS для {domain_name}")
            raise HTTPError(500, f"Ошибка при сохранении данных WHOIS для {domain_name}: {str(e)}")

        # print(json.dumps(whois_data, indent=4, ensure_ascii=False))
        return f"Данные с {domain_name} успешно сохранены"  # сообщение об успешном сохранении

    except Exception as e:
        logging.error(f"Ошибка при выполнении запроса WHOIS для {domain_name}: {str(e)}")
        raise HTTPError(500, f"Произошла ошибка: {str(e)}")

    finally:
        if driver:
            driver.quit()
