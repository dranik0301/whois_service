from bottle import route, run, request, template
import logging

from whois import whois_data_check

logging.basicConfig(level=logging.INFO)


@route('/')
def index():
    return template('index')


@route('/result', method='POST')
def result():
    text = request.forms.get('text')
    logging.info(f"Получен запрос на WHOIS для домена: {text}. Проверяем корректность доменного имени.")

    whois_data = whois_data_check(text)
    return template('result', result=whois_data)


run(host='localhost', port=8080, debug=True)
