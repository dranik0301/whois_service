from bottle import run, Bottle, response

from whois_service_cURL.services.whois import whois_data_check

app = Bottle()


@app.route('/lookup_whois/<domain_name>')
def lookup(domain_name):
    whois_data = whois_data_check(domain_name)
    response.content_type = 'application/json'
    return whois_data


run(app, host='localhost', port=8080)
