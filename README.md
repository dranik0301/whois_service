# WHOIS API

## 📌 Описание
Этот проект представляет собой API для получения информации WHOIS с сайта [ps.kz](https://www.ps.kz).
API написан с использованием **FastAPI**, **BeautifulSoup**, **SQLite** и контейнеризирован с **Docker**.

## 🚀 Установка и запуск

### 🔧 1. Клонирование репозитория
```sh
git clone https://github.com/your-repo/whois-api.git
cd whois-api
```

### 🛠 2. Установка зависимостей
Перед запуском локально убедись, что установлен Python 3.11+ и установи зависимости:
```sh
pip install -r requirements.txt
```

### ▶ 3. Запуск сервера
```sh
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Теперь API доступно по адресу: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 🐳 Запуск через Docker

### 1️⃣ Сборка образа
```sh
docker build -t whois-api .
```

### 2️⃣ Запуск контейнера
```sh
docker run -p 8000:8000 whois-api
```

Теперь API доступно на `http://localhost:8000`

---

## 📡 API Эндпоинты

### 🔍 Получение информации WHOIS
**GET /lookup_whois?domain=example.com**

#### 📥 Запрос:
```sh
curl -X 'GET' 'http://localhost:8000/lookup_whois?domain=example.com' -H 'accept: application/json'
```

#### 📤 Ответ:
```json
{
  "domen_info": "example.com",
  "status": {"Статус": "Активен"},
  "registrar": "Some Registrar",
  "registrant": {"Имя": "John Doe", "Email": "john@example.com"},
  "administrative_contact": {"Имя": "Jane Doe", "Email": "jane@example.com"},
  "server_name": ["ns1.example.com", "ns2.example.com"],
  "created": "2020-01-01",
  "expiration_date": "2025-01-01",
  "transfer_date": "2023-01-01"
}
```

---

## 📝 Файлы проекта
- `main.py` — основной файл FastAPI
- `parser/parser.py` — парсинг данных с ps.kz
- `structuring_data/structuring_data.py` — структурирование данных WHOIS
- `create_table/create_table.py` — база данных SQLite
- `Dockerfile` — конфигурация для контейнера
- `requirements.txt` — список зависимостей

---

## 🛠 Зависимости
Проект использует:
- `FastAPI` — фреймворк для создания API
- `BeautifulSoup4` — парсер HTML
- `SQLite` — встроенная база данных
- `Docker` — контейнеризация

### 📦 Установка зависимостей вручную
```sh
pip install fastapi requests beautifulsoup4 sqlite3 uvicorn
```

---

## 📜 Лицензия
Этот проект распространяется под лицензией MIT.

