def create_data(data):
    return {
        "domen_info": data.get("domen_info", "Отсутствует"),
        "status": data.get("status", {}),
        "registrar": data.get("registrar", "Отсутствует"),
        "registrant": data.get("registrant", {}),
        "administrative_contact": data.get("administrative_contact", {}),
        "server_name": data.get("server_name", []),
        "created": data.get("created", "Отсутствует"),
        "expiration_date": data.get("expiration_date", "Отсутствует"),
        "transfer_date": data.get("transfer_date", "Отсутствует")
    }
