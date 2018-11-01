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

# TODO: add information on why this import must go here.
# this import must go here
import models

def main():

    # So this is a very import place in the code, because we are asking for user input!
    # Users are stupid, users are evil, users are clever, and we must never trust user
    # input blindly.
    #
    # If someone was to QA this application, this would be the first
    # place they focus ala https://twitter.com/sempf/status/514473420277694465
    #
    # So this is the like the gate to the application,
    # and if handle problems upfront here, we can simply our lives deeper in the code.
    #
    # So now what is the way to ensure that user input a valid ASIN,
    # and if they didn't not letting then invalid ASIN proceed any deeper into the code?
    #
    # This is also a classic place to add some tests. A test that would input a proper ASIN,
    # and work correctly, and then an invalid ASIN, and error in the appropiate way.
    #
    # This way we can ensure this functionality stays in tact, even if we start moving
    # around and refactoring the code. This would also have the benefit of documenting the various
    # scenarios the program knows how to respond to.
    asin = input("Please enter a vaild ASIN: ")

    # I love the simplicity of this method, you call the amazon object to create the url,
    # and pass it the ASIN. It couldn't be simpler! .....however I am curious about what this
    # URL looks like and what its for. This would be great to have as a comment right here.
    url =  amazon.create_url(asin)

    result = amazon.scrape(url, asin)

    # So when I first read this, I wonder what reg means. It might be obvious,
    # but nothing is common to mind right now, and it's also good to think about
    # variable names being read by someone 5 years from now, who has no idea what the code does
    #
    # Also one think I notice is the result opject, has to properties accessed on it, the name,
    # which corresponds to the Item name apparently, and the count,
    # which corresponds to the customer_reviews_count
    #
    # the name make sense in the abstract, but the count being for the customer_reviews_count
    # has a lot of implications on the rest of the code.
    #
    # If the result of amazon.scape(url) is a result, whose count is customer reviews count
    # Then that URL must always have customer reviewers, scrape method should always being
    # storing the customer_reviews_count as count.
    #
    # The problem is the mixing of abstraction levels. Something very generic like scrape url,
    # mapping to the count of customer review counts.
    # and this brings us to the constant programming joke: https://martinfowler.com/bliki/TwoHardThings.html
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
