from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import amzscraper as amazon
import urls
import asin_validation

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def main():

    selection = "y"
    while selection == "y":
        try:
            asin = asin_validation.get_valid_asin()
            # Concatonates a standard Amazon Url with no extras with the ASIN
            # at the end for use in Scraping
            url = urls.create_url(asin)
            amazon.scrape(url, asin)
        except:
            print("An Error Occured While Scraping")
            raise
        selection = input("Do you have another ASIN? (y/n) ")
        if selection == "n":
            break


if __name__ == "__main__":
    main()
