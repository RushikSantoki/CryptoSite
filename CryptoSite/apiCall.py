import requests
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from CryptoSite.models import Status, Icons
from pycoingecko import CoinGeckoAPI


def downloadingData():
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
        'start': '1',
        'limit': '500',
        'convert': 'CAD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': 'f4296060-5178-49c8-9694-e413de103353',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        # print(data)
        list_price = {}
        for d in data['data']:
            if d['name'] == 'Bitcoin':
                list_price['Bitcoin'] = round(d['quote']['CAD']['price'], 2)
            if d['name'] == 'Ethereum':
                list_price['Ethereum'] = round(d['quote']['CAD']['price'], 2)
            if d['name'] == 'Dogecoin':
                list_price['Dogecoin'] = round(d['quote']['CAD']['price'], 2)
        return list_price
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def downloadingSpecificData(slug, id):
    if (checkModel(slug) == 0):
        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
            'slug': slug,
            'convert': 'CAD'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': 'f4296060-5178-49c8-9694-e413de103353',
        }

        session = Session()
        session.headers.update(headers)

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            print(data)
            Status(id,
                   str(data['data'][id]['id']),
                   data['data'][id]['name'],
                   data['data'][id]['symbol'],
                   str(round(data['data'][id]['quote']['CAD']['price'], 2)),
                   str(round(data['data'][id]['quote']['CAD']['percent_change_24h'], 3)),
                   str(round(data['data'][id]['quote']['CAD']['percent_change_7d'], 3)),
                   str(round(data['data'][id]['quote']['CAD']['percent_change_1h'], 3)),
                   str(data['data'][id]['quote']['CAD']['market_cap']),
                   str(round(data['data'][id]['quote']['CAD']['percent_change_30d'], 3)),
                   str(round(data['data'][id]['quote']['CAD']['percent_change_60d'], 3)),
                   str(round(data['data'][id]['quote']['CAD']['percent_change_90d'], 3))
                   ).save()
        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)
    else:
        print('Value Already exists')


def downloadIcons(slugs):
    try:
        url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false"
        data = requests.get(url).json()
        print(data)
        for index, slug in enumerate(slugs):
            for i in data:
                if slug == i['id']:
                    Icons(index, i['name'], i['image']).save()
                    continue
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


def checkModel(val):
    try:
        if Status.objects.filter(currency_name=val).exists():
            return 1
        else:
            return 0
    except:
        print('Error')
