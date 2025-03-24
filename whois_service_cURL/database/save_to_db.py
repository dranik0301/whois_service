import sqlite3
import json
import logging

logging.basicConfig(level=logging.INFO)

conn = sqlite3.connect('../whois.db')
cursor = conn.cursor()

def save_to_db(whois_data: dict[str, any]) -> bool:
    try:
        status_json = json.dumps(whois_data.get('statuses'), ensure_ascii=False)
        registrant_json = json.dumps(whois_data.get('registrant'), ensure_ascii=False)
        admin_contact_json = json.dumps(whois_data.get('admin'), ensure_ascii=False)
        server_name_json = json.dumps(whois_data.get('nameservers'), ensure_ascii=False)

        values = (
            whois_data.get('domain'),
            status_json,
            whois_data.get('currentRegistrar'),
            registrant_json,
            admin_contact_json,
            server_name_json,
            whois_data.get('createdAt'),
            whois_data.get('updatedAt'),
            whois_data.get('expiresAt'),
            whois_data.get('transferredAt')
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
        raise
