from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
import amzscraper as amazon

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Valid ASINs are a combination of 10 Letters and Integers
# Not sure yet how to check is a seemingly valid ASIN is actually
# valid without first trying to scrape it
# example of seemingly valid ASIN = B011111111
def get_valid_asin():
    while True:
        asin = input('Please enter a vaild ASIN: ')
        if not len(asin) == 10:
            print('Invalid ASIN')
            continue
        else:
            return asin

def main():

    selection = 'y'
    while selection =='y':
        try:
            asin = get_valid_asin()
            # Concatonates a standard Amazon Url with no extras with the ASIN
            # at the end for use in Scraping
            url =  amazon.create_url(asin)
            amazon.scrape(url, asin)
        except:
            print('An Error Occured While Scraping')
        # if the first item fails to store in DB all subsequent items fail
        selection = input('Do you have another ASIN? (y/n) ')
        if selection == 'n':
            break

if __name__ == '__main__':
    main()
