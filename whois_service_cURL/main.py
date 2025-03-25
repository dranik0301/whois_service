from bottle import run, Bottle, response

from services.whois import WhoisService

app = Bottle()
whois_service = WhoisService()


@app.route('/lookup_whois/<domain_name>')
def lookup(domain_name):
    response.content_type = 'application/json'
    return whois_service.whois_data_check(domain_name)


run(app, host='localhost', port=8080)
