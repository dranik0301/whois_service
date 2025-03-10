import sqlite3

conn = sqlite3.connect('../whois.db')


def create_table():
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS whois_data (
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
        return True

    except Exception as e:
        print(f'Ошибка при создании таблицы: {str(e)}')
        raise f'{str(e)}'
