# Пример данных
```json
{
    "data": {
        "vitrina": {
            "domains": {
                "whois": {
                    "status": {
                        "domainAvailable": false
                    },
                    "data": {
                        "domain": "example.kz",
                        "statuses": [
                            "clientTransferProhibited",
                            "clientDeleteProhibited",
                            "clientUpdateProhibited",
                            "clientRenewProhibited"
                        ],
                        "currentRegistrar": "Registrar Name",
                        "registrant": {
                            "name": "Registrant Name",
                            "organization": "Registrant Org",
                            "country": "KZ",
                            "city": "City Name",
                            "postalCode": "000000",
                            "street": "Street Address",
                            "phone": "+7 000 0000000",
                            "email": "email@example.com"
                        },
                        "admin": {
                            "name": "Admin Name",
                            "organization": "Admin Org",
                            "country": "KZ",
                            "city": "City Name",
                            "postalCode": "000000",
                            "street": "Street Address",
                            "phone": "+7 000 0000000",
                            "email": "email@example.com"
                        },
                        "nameservers": [
                            "ns1.example.kz",
                            "ns2.example.kz"
                        ],
                        "createdAt": "2000-01-01T00:00:00.000Z",
                        "updatedAt": "2000-01-01T00:00:00.000Z",
                        "expiresAt": "2030-01-01T00:00:00.000Z",
                        "transferredAt": "2010-01-01T00:00:00.000Z"
                    }
                }
            }
        }
    }
}
```

## Установка зависимостей

Перед запуском проекта установите необходимые зависимости:

```sh
pip install -r requirements.txt
```

## Запуск проекта локально

После установки зависимостей запустите приложение:

```sh
python main.py
```

Пример запроса:

```sh
curl http://localhost:8080/lookup_whois/example.com
```

## Запуск проекта через Docker

### 1. Сборка Docker-образа

```sh
docker build -t whois_service_cURL .
```

### 2. Запуск контейнера

```sh
docker run -p 8080:8080 whois_service_cURL
```

### 3. Запуск через docker-compose

Если в проекте есть `docker-compose.yml`, можно запустить его с помощью:

```sh
docker-compose up --build
```

## Пример запроса

Чтобы получить WHOIS-данные о домене, выполните:

```sh
curl http://localhost:8080/lookup_whois/example.com
```

