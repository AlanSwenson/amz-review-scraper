import time

import requests
import bs4
import lxml

from amz_review_scraper.config import proxies, HEADER


def boil_soup(url, asin):
    # Try up to 3 times if we get blocked by Amazon
    for i in range(2):
        raw_html = requests.get(url, headers=HEADER, proxies=proxies)
        if raw_html.status_code == 200:
            soup = bs4.BeautifulSoup(raw_html.text, "lxml")
            return soup
        elif raw_html.status_code == 404:
            break
        else:
            print("Trying Again in 1 second")
            time.sleep(1)
    return raw_html
