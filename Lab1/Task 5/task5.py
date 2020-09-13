import requests
import xml.etree.ElementTree as Tree
import datetime as dt


def get_currency_rates_data(date: str) -> Tree:
    req = requests.get(f"http://www.cbr.ru/scripts/XML_daily.asp?date_req={date}")
    return Tree.fromstring(req.text)


def parse_required_data() -> list:
    starting_date = dt.date(2020, 3, 1)
    ending_date = dt.date(2020, 7, 1)
    step = dt.timedelta(days=1)

    data = []
    required_currency = ["USD", "EUR", "INR", "UAH"]

    while starting_date <= ending_date:
        tree = get_currency_rates_data(starting_date.strftime("%d/%m/%Y"))
        for leaf in tree:
            if leaf[1].text in required_currency:
                currency_name = leaf[3].text
                cost = round(float(leaf[4].text.replace(',', '.')) / float(leaf[2].text), 4)
                data.append([starting_date.strftime("%d/%m/%Y"), currency_name, cost])

        starting_date += step

    return data


def main():
    data = parse_required_data()
    for item in data:
        print(item)


if __name__ == '__main__':
    main()
