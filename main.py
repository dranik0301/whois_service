import requests
import logging
from fastapi import FastAPI, HTTPException
from bs4 import BeautifulSoup
from typing import Dict

from structuring_data.structuring_data import create_data
from parser.parser import get_whois_data
from create_table.create_table import create_table, save_to_db

# Logging configuration
logging.basicConfig(level=logging.INFO)

app = FastAPI()
create_table()

@app.get("/lookup_whois")
def lookup_whois(domain: str) -> Dict[str, str]:
    logging.info(f"Received WHOIS lookup request for domain: {domain}")

    url = f"https://www.ps.kz/domains/whois/result?q={domain}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error fetching WHOIS data for {domain}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching WHOIS data: {str(e)}")

    soup = BeautifulSoup(response.text, 'html.parser')
    raw_data = get_whois_data(soup)

    whois_data = create_data(raw_data)

    try:
        save_to_db(whois_data)
        logging.info(f"WHOIS data for {domain} successfully saved to the database")
    except Exception as e:
        logging.error(f"Error saving WHOIS data for {domain}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error saving data to the database: {str(e)}")

    return whois_data

if __name__ == "__main__":
    import uvicorn
    logging.info("Starting FastAPI server...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
