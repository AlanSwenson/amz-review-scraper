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
# this import must go here
import models

def main():
    asin = input("Please enter a vaild ASIN: ")
    url =  amazon.create_url(asin)

    result = amazon.scrape(url, asin)

    reg = models.Items(name=result.name, customer_reviews_count=result.count, asin=asin)

    db.session.add(reg)
    db.session.commit()


    selection = input("Do you have another ASIN? (y/n) ")
    if selection == 'y':
        print("Cool")
    else:
        sys.exit()

if __name__ == "__main__":
    main()
