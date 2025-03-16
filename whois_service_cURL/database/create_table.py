import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('../whois.db')


def table_exists():
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='whois_data';")
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def create_table():
    if table_exists():
        logging.info("Таблица whois_data уже существует. Пропускаем создание.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE whois_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                domain_name TEXT NOT NULL,
                status TEXT,
                registrator TEXT,
                registrant TEXT,
                administrative_contact TEXT,
                server_name TEXT,
                created TEXT,
                last_modified TEXT,
                expiration_date TEXT,
                transfer_date TEXT
            )
        ''')
        conn.commit()
        logging.info("Таблица whois_data успешно создана.")
    except Exception as e:
        logging.error(f'Ошибка при создании таблицы: {str(e)}')
    finally:
        conn.close()
