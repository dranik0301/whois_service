from bottle import run, Bottle, response
import logging

from app.services.whois import whois_data_check

logging.basicConfig(level=logging.INFO)

app = Bottle()


@app.route('/lookup_whois/<domain_name>')
def lookup(domain_name):
    whois_data = whois_data_check(domain_name)
    response.content_type = 'application/json'

    return whois_data


run(app, host='localhost', port=8080, debug=True, reloader=True)
