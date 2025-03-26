import sqlite3
import json
import logging

logging.basicConfig(level=logging.INFO)


class WhoisDatabase:
    def __init__(self, db_path: str = "whois.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.create_table()

    def table_exists(self) -> bool:
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='whois_data';")
        return self.cursor.fetchone() is not None

    def create_table(self):
        if self.table_exists():
            logging.info("Таблица whois_data уже существует. Пропускаем создание.")
            return

        try:
            self.cursor.execute('''
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
                    transfer_date TEXT,
                    create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
            logging.info("Таблица whois_data успешно создана.")
        except Exception as e:
            logging.error(f'Ошибка при создании таблицы: {e}')

    def save_to_db(self, whois_data: dict[str, any]) -> bool:
        try:
            values = (
                whois_data.get('domain'),
                json.dumps(whois_data.get('statuses'), ensure_ascii=False),
                whois_data.get('currentRegistrar'),
                json.dumps(whois_data.get('registrant'), ensure_ascii=False),
                json.dumps(whois_data.get('admin'), ensure_ascii=False),
                json.dumps(whois_data.get('nameservers'), ensure_ascii=False),
                whois_data.get('createdAt'),
                whois_data.get('updatedAt'),
                whois_data.get('expiresAt'),
                whois_data.get('transferredAt')
            )

            self.cursor.execute('''
                INSERT INTO whois_data (
                    domain_name, status, registrator, registrant,
                    administrative_contact, server_name, created, last_modified, expiration_date, transfer_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)

            logging.info("Данные сохранены в SQL.")

            self.conn.commit()
            return True

        except Exception as e:
            logging.error(f'Ошибка при сохранении данных: {e}')
            return False

    def close(self):
        self.conn.commit()
        self.conn.close()
        logging.info("Соединение с базой данных закрыто.")

# WhoisDatabase().save_to_db()
