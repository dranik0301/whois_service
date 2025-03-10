FROM python:3.12

WORKDIR /app

COPY . /app

RUN pip install bottle whois

EXPOSE 8080

CMD ["python", "main.py"]
