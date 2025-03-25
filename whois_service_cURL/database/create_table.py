import sqlite3
import logging

logging.basicConfig(level=logging.INFO)


class WhoisDatabaseCreate:
    def __init__(self, db_path: str = "whois.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

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

    def close(self):
        self.conn.close()
