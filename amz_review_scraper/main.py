import sys

import amzscraper as amazon
import urls
import asin_validation
import get_soup

from app import create_app, db


app = create_app()
app.app_context().push()


def main():

    selection = "y"
    while selection == "y":
        try:
            while True:
                asin = asin_validation.get_valid_asin()
                # Concatonates a standard Amazon Url with no extras with the ASIN
                # at the end for use in Scraping
                url = urls.create_url(asin)
                soup = get_soup.boil_soup(url, asin)
                if soup.status_code != None:
                    print(f"Status Code: {soup.status_code}")
                    continue
                else:
                    amazon.scrape(soup, asin)
                    break
        except:
            print("An Error Occured While Scraping")
            raise
        selection = input("Do you have another ASIN? (y/n) ")
        if selection == "n":
            break


if __name__ == "__main__":
    main()
