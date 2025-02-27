import sqlite3
import json


def create_table():
    conn = sqlite3.connect('whois.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS whois_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domen_info TEXT NOT NULL,
            status TEXT,
            registrar TEXT,
            registrant TEXT,
            administrative_contact TEXT,
            server_name TEXT,
            created TEXT,
            expiration_date TEXT,
            transfer_date TEXT
        )
    ''')
    conn.commit()
    conn.close()


def save_to_db(whois_data):
    conn = sqlite3.connect('whois.db')
    cursor = conn.cursor()

    # Преобразуем вложенные структуры в JSON
    status_json = json.dumps(whois_data.get("status", {}), ensure_ascii=False)
    registrant_json = json.dumps(whois_data.get("registrant", {}), ensure_ascii=False)
    admin_contact_json = json.dumps(whois_data.get("administrative_contact", {}), ensure_ascii=False)
    server_name_json = json.dumps(whois_data.get("server_name", []), ensure_ascii=False)

    values = (
        whois_data["domen_info"],
        status_json,
        whois_data.get("registrar", "Отсутствует"),
        registrant_json,
        admin_contact_json,
        server_name_json,
        whois_data.get("created", "Отсутствует"),
        whois_data.get("expiration_date", "Отсутствует"),
        whois_data.get("transfer_date", "Отсутствует")
    )

    cursor.execute('''
        INSERT INTO whois_data (
            domen_info, status, registrar, registrant,
            administrative_contact, server_name, created, expiration_date, transfer_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', values)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_table()
