import csv
import requests


def fresh_currency():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data_from_json = response.json()

    with open("output.csv", 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=';')
        rates = data_from_json[0]['rates']

        for rate in rates:
            currency = rate['currency']
            code = rate['code']
            bid = rate['bid']
            ask = rate['ask']
            print(currency, code, bid, ask)
            writer.writerow([currency, code, bid, ask])


fresh_currency()