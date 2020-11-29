import argparse
from sys import argv
import csv
from os import makedirs, environ
import requests


TOKEN = environ["UP_KEY"]


def parse_transaction(transaction):
    '''
    Extract desired information from transactions here
    '''
    att = transaction['attributes']

    # ignore savings <-> spending transactions
    if att['rawText'] is None:
        return None

    return {
        'date': att['createdAt'].split("T")[0],
        'amount': att['amount']['value'],
        'currency': att['amount']['currencyCode'],
        'description': att['rawText'],
    }


def parse_response(response: requests.Response):
    '''
    iterate over the transactions, also returning the link to the next page
    '''
    json = response.json()
    transactions = [parse_transaction(i) for i in json['data']]
    transactions = list(filter(lambda t: t is not None, transactions))
    next_link = json['links']['next']
    return transactions, next_link


def get_transactions(start_date: str, end_date: str, url: str = None):
    headers = {"Authorization": "Bearer {}".format(TOKEN)}
    try:
        if url is None:
            response = requests.get(
                url="https://api.up.com.au/api/v1/transactions",
                params={
                    "filter[since]": "{}T00:00:00+10:00".format(start_date),
                    "filter[until]": "{}T23:59:59+10:00".format(end_date),
                    "page[size]": "100"
                },
                headers=headers,
            )
        else:
            # url is given
            response = requests.get(url=url, headers=headers)
        return parse_response(response)
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def fetch_csv(start_date: str, end_date: str):
    results, next_link = get_transactions(start_date, end_date)
    while next_link is not None:
        data, next_link = get_transactions(start_date, end_date, next_link)
        results.extend(data)

    if len(results) == 0:
        print("No transactions")
        exit()

    keys = results[0].keys()

    makedirs("output", exist_ok=True)
    with open('output/{}_{}.csv'.format(start_date, end_date), 'w', newline='') as f:
        writer = csv.DictWriter(f, keys)
        writer.writeheader()
        writer.writerows(results)


parser = argparse.ArgumentParser(
    usage="UP_KEY=up:yeah:XXXX main.py [-h] start=YYYY-MM-DD end=YYYY-MM-DD")
parser.add_argument("start", type=str, help="YYYY-MM-DD")
parser.add_argument("end", type=str, help="YYYY-MM-DD")
args = parser.parse_args()
if TOKEN == "":
    exit("Must specify environment variable: UP_KEY, see readme")

fetch_csv(args.start, args.end)
