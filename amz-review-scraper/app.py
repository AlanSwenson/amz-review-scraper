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

# this import must go here because
# the db must be created before models are imported
import models

def main():
    while True:
        # Valid ASINs are a combination of 10 Letters and Integers
        # Not sure yet how to check is a seemingly valid ASIN is actually
        # valid without first trying to scrape it
        # example of seemingly valid ASIN = B011111111
        asin = input('Please enter a vaild ASIN: ')
        if not len(asin) == 10:
            print('Invalid ASIN')
            continue
        else:
            # Concatonates a standard Amazon Url with no extras with the ASIN
            # at the end for use in Scraping
            url =  amazon.create_url(asin)
            break

    try:
        result = amazon.scrape(url, asin)
    except:
        print('An Error Occured While Scraping')

    try:
        scraped_item = models.Items( name=result.name,
                                customer_reviews_count=result.reviews,
                                asin=asin)

        db.session.add(scraped_item)
        db.session.commit()
    except:
        print('An Error Occured While Saving Item to DB')

    selection = input('Do you have another ASIN? (y/n) ')
    if selection == 'y':
        print('Cool')
    else:
        sys.exit()

if __name__ == '__main__':
    main()
