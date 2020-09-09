import requests
import csv


def get_json_from_pastebin(url: str) -> list:
    return requests.get(url).json()


def json_to_csv(json_data: list) -> None:
    sales_csv = open("sales.csv", "w")
    csv_writer = csv.writer(sales_csv, delimiter=",")

    headers = ["item", "country", "year", "sales"]
    csv_writer.writerow(headers)

    for elem in json_data:
        content = list(elem.values())
        item = content[0]
        years_and_sales = content[1]

        for country in years_and_sales:
            years = list(reversed(years_and_sales[country].keys()))
            sales = list(reversed(years_and_sales[country].values()))

            while years or sales:
                row = [item, country, years.pop(), sales.pop()]
                csv_writer.writerow(row)
                row.clear()

    sales_csv.close()


def main():
    json_data = get_json_from_pastebin("https://pastebin.com/raw/edzB88Px")
    json_to_csv(json_data)
    with open("sales.csv") as f:
        csv_reader = csv.reader(f)
        for row in csv_reader:
            print(row if row != [] else '\n', end='')


if __name__ == '__main__':
    main()
