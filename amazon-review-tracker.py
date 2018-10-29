from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import sys
import os
import amzscraper as amazon

app = Flask(__name__)

def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

# the values of those depend on your setup
POSTGRES_URL = get_env_variable("POSTGRES_URL")
POSTGRES_USER = get_env_variable("POSTGRES_USER")
POSTGRES_PW = get_env_variable("POSTGRES_PW")
POSTGRES_DB = get_env_variable("POSTGRES_DB")

DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)

print('URL :' + DB_URL)

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # silence the deprecation warning

db = SQLAlchemy(app)

class Entry(db.Model):
    __tablename__ = "reviews"
    name = db.Column(db.String)
    customer_reviews_count = db.Column(db.Integer) 
    asin = db.Column(db.String(10), primary_key=True)

def main():
    asin = input("Please enter a vaild ASIN: ")
    url =  amazon.create_url(asin)
    result = amazon.scrape(url)
    print(url)
    print(result.count)


    reg = Entry(name=result.name, customer_reviews_count=result.count, asin=asin)

    db.session.add(reg)
    db.session.commit()


    selection = input("Do you have another ASIN? (y/n) ")
    if selection == 'y':
        print("Cool")
    else:
        sys.exit()

if __name__ == "__main__":
    main()
