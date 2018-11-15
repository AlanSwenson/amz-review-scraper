import time

import requests
import bs4
import lxml

from config import proxies, HEADER


def boil_soup(url, asin):
    for i in range(2):
        raw_html = requests.get(url, headers=HEADER, proxies=proxies)
        if raw_html.status_code == 200:
            soup = bs4.BeautifulSoup(raw_html.text, "lxml")
            return soup
        else:
            time.sleep(1)
            print("Trying Again in 1 second")
    return raw_html
