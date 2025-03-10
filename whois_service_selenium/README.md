# README

## Установка Selenium

Для работы с Selenium в проекте можно использовать один из двух способов установки:

### Способ 1: Установка через неофициальную документацию Selenium

Подробную инструкцию можно найти по ссылке:  
[https://selenium-python.readthedocs.io/installation.html#introduction](https://selenium-python.readthedocs.io/installation.html#introduction)

### Способ 2: Установка через Chocolatey

1. Установите Chocolatey: [https://chocolatey.org/install](https://chocolatey.org/install)
2. Установите Google Chrome: [https://community.chocolatey.org/packages/googlechrome](https://community.chocolatey.org/packages/googlechrome)
3. Установите ChromeDriver: [https://community.chocolatey.org/packages/chromedriver](https://community.chocolatey.org/packages/chromedriver)

---

## Установка зависимостей

Проект содержит файл `requirements.txt`, в котором указаны все необходимые зависимости. Чтобы установить их, выполните команду:

```sh
pip install -r requirements.txt
```

---

## Запуск проекта через Docker

### 1. Сборка Docker-образа

```sh
docker build -t bottle-whois .
```

### 2. Запуск контейнера

```sh
docker run -p 8080:8080 bottle-whois
```

### 3. Запуск через `docker-compose`

```sh
docker-compose up --build
```


