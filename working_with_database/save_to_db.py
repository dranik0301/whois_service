import sqlite3
import json
import logging


def save_to_db(whois_data) -> None:
    try:
        conn = sqlite3.connect('whois.db')
        cursor = conn.cursor()

        status_json = json.dumps(whois_data.get("status", None), ensure_ascii=False)
        registrant_json = json.dumps(whois_data.get("registrant", None), ensure_ascii=False)
        admin_contact_json = json.dumps(whois_data.get("administrative_contact", None), ensure_ascii=False)
        server_name_json = json.dumps(whois_data.get("server_name", None), ensure_ascii=False)

        values = (
            whois_data.get("domain_name", None),
            status_json,
            whois_data.get("registrator", None),
            registrant_json,
            admin_contact_json,
            server_name_json,
            whois_data.get("created", None),
            whois_data.get("last_modified", None),
            whois_data.get("expiration_date", None),
            whois_data.get("transfer_date", None)
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
        logging.error(f"Ошибка при сохранении данных WHOIS в БД: {str(e)}")
        return False

    finally:
        conn.close()
