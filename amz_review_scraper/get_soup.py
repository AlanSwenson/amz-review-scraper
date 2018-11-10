import requests
import bs4
import lxml
from config import proxies, HEADER


def boil_soup(url, asin):
    raw_html = requests.get(url, headers=HEADER, proxies=proxies)
    if raw_html.status_code != 200:
        return raw_html
    else:
        soup = bs4.BeautifulSoup(raw_html.text, "lxml")
        return soup
