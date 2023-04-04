import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime


url = 'http://www.cbr.ru/scripts/XML_daily.asp?'
date = datetime.today().strftime("%d/%m/%Y")
response = requests.get(url, params={'date_req': date})


def form_valute_list(url, date):
    global response
    if response:
        data = bs(response.text, features='xml')
        headers = ('NumCode', 'CharCode', 'Nominal', 'Name', 'Value')
        valutes = {}
        for valute in data.find_all('Valute'):
            valutes[valute.CharCode.text] = dict(zip(headers, [float(i.text.replace(",", '.')) if "," in i.text
                                                               else int(i.text) if i.text.isdigit() else i.text for i in valute]))
        return valutes
    else:
        raise ValueError(f'{response.status_code}')


valutes = form_valute_list(url, date)


def getCourse(code: str) -> int|str:
    try:
        return round(
            valutes[code]['Nominal'] * valutes[code]['Value'],
            2)
    except KeyError:
        return {"detail": "несуществующий код вылюты"}


def convert(valute_from: str, valute_to: str, amount: int, valute_list=form_valute_list(url, date)) -> int:
    if valute_from == valute_to:
        return amount
    match valute_from:
        case 'RUB':
            val = valute_list[valute_to]
            return amount / (val['Value'] / val['Nominal'])
        case _:
            val = valute_list[valute_from]
            match valute_to:
                case 'RUB':
                    return amount * (val['Value'] / val['Nominal'])
                case _:
                    return convert('RUB' , valute_to, amount * (val['Value'] / val['Nominal']))


def site_request(url='http://127.0.0.1:8000/physics/mechanics/newton2/') -> list:
    with requests.Session() as s:
        s.auth = ('admin', 'password')
        data = {'find_mark': 'f', 'uskorenie': '100', 'massa': '500', 'massa_si': 'kg', 'uskorenie_si': 'm/s^2', 'nums_comma': '3'}
        response = s.get(url, data=data)
        html = bs(response.text, 'lxml')
        text = html.find_all('h4')
        return text


if __name__ == '__main__':
    valute_list = form_valute_list(url, date)
    valute_from = input('Какую валюту перевести? (введите буквенный код)\t...')
    valute_to = input('В какую валюту перевести? (введите буквенный код)\t...')
    amount = int(input('Количество денежных средств валюты\t...'))
    result = round(convert(valute_from.upper(), valute_to.upper(), amount), 2)
    print(f"{amount} {valute_from} = {result} {valute_to}")

