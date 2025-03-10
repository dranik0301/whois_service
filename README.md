# Установка зависимостей

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

