import json
import logging

from database.create_table import WhoisDatabaseCreate

logging.basicConfig(level=logging.INFO)


class WhoisDatabaseSave:
    def __init__(self, db_path: str = "whois.db"):
        self.db = WhoisDatabaseCreate(db_path)

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

            self.db.cursor.execute('''
                    INSERT INTO whois_data (
                        domain_name, status, registrator, registrant,
                        administrative_contact, server_name, created, last_modified, expiration_date, transfer_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', values)

            self.db.conn.commit()
            return True

        except Exception as e:
            logging.error(f'Ошибка при сохранении данных: {e}')
            return False

    def close(self):
        self.db.close()
