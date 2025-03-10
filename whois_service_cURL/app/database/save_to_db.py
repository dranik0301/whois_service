import sqlite3
import json
import logging

logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('../whois.db')


def save_to_db(whois_data: dict[str:any]) -> bool:
    try:
        cursor = conn.cursor()

        status_json = json.dumps(whois_data.get('statuses', None), ensure_ascii=False)
        registrant_json = json.dumps(whois_data.get('registrant', None), ensure_ascii=False)
        admin_contact_json = json.dumps(whois_data.get('admin', None), ensure_ascii=False)
        server_name_json = json.dumps(whois_data.get('nameservers', None), ensure_ascii=False)

        values = (
            whois_data.get('domain', None),
            status_json,
            whois_data.get('currentRegistrar', None),
            registrant_json,
            admin_contact_json,
            server_name_json,
            whois_data.get('createdAt', None),
            whois_data.get('updatedAt', None),
            whois_data.get('expiresAt', None),
            whois_data.get('transferredAt', None)
        )

        cursor.execute('''
            INSERT INTO whois_data (
                domain_name, status, registrator, registrant,
                administrative_contact, server_name, created, last_modified, expiration_date, transfer_date
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', values)

        conn.commit()
        return True

    except Exception as e:
        logging.error(f'Ошибка при сохранении данных WHOIS в БД: {str(e)}')
        raise f'{str(e)}'
