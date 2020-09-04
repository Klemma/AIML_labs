import requests
import re


def get_txt_from_url(url: str) -> str:
    return requests.get(url).text


if __name__ == '__main__':
    content = get_txt_from_url("https://pastebin.ubuntu.com/p/QvcQ6Q2QsK/")
    pattern = r'[A-Z,a-z,<,>,",/,=,!,-,.,:,;]'
    repl = ""
    content = re.sub(pattern, repl, content)
    print(content)
