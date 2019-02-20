Review Scraper for Amazon
===
![Programming language: python](https://img.shields.io/badge/python-3.6-blue.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Build Status](https://travis-ci.org/AlanSwenson/amz-review-scraper.svg?branch=master)](https://travis-ci.org/AlanSwenson/amz-review-scraper) [![Coverage Status](https://coveralls.io/repos/github/AlanSwenson/amz-review-scraper/badge.svg)](https://coveralls.io/github/AlanSwenson/amz-review-scraper)

##### Table of Contents  
[What do I do?](#what_do_i_do)  
[Install](#install)  
[Setup](#setup)   
[Local Usage](#local_usage)   
[Deployed Usage](#deployed_usage)   
[More things you should know](#more)   
[How to contribute](#contribute)


<a name="what_do_i_do"/>
## What do I do?

This project scrapes Amazon listings for recent reviews of specified products (ASIN) and stores them in a Postgres DB

##### Future Features

- Emails users when their subscribed ASIN has a new review
- Add way for users to stop tracking an ASIN they were tracking
- Use Zappa to make the scrape function its own lambda
- Scraper should run on its own periodically to check for new reviews for each ASIN

##### Future non-feature enhancements
- Add Web Testing with Selenium
- Get testing coverage closer to 100%

<a name="install"/>
## Install

This project uses [pipenv](https://github.com/pypa/pipenv) for virtual environments

Navigate to the directory you want to install the project

```bash
git clone <project clone url>
pip install pipenv
cd amz-review-scraper
pipenv shell
pipenv sync

```

<a name="setup"/>
## Setup

#### Create empty PostreSQL databases
This project uses Postgres as it's database of choice. There are 3 environments set up and for each one you will need to setup a Postgres DB. You will need **development** and **testing** locally and **production** for your deployment.  Use the credentials from each your new databases to complete the .env file below.  My **production** database is setup on RDS but you could choose to do things differently.
<a name="local_usage"/>
# Local Usage

#### Set up a .env file
~~~~
#environment setups

#development
export DEV_SQLALCHEMY_DATABASE_URI= "postgresql://your_development_postgres_url_connection"
export DEV_DEBUG = True
export DEV_LOGIN_BASE_URL="http://127.0.0.1:5000"

#testing
export TESTING_SQLALCHEMY_DATABASE_URI= "postgresql://postgres:@localhost:5432/travis_ci_test"
export TESTING_DEBUG = True
export TESTING_TESTING = True
export TESTING_LOGIN_BASE_URL="http://127.0.0.1:5000"

#production
export PROD_SQLALCHEMY_DATABASE_URI= "postgresql://your_production_postgres_url_connection"
export PROD_LOGIN_BASE_URL="https://your_production_url.com"

#proxy variables
export http="http://proxyservice"
export https="https://proxyservice"

#ensuring UTF-8 to make sure Black works correctly
export LC_ALL=en_US.utf-8
export LANG=en_US.utf-8

#Flask variables
export FLASK_APP=run.py
export FLASK_SECRET_KEY="a_super secret_key"

#Flask-s3 variables for storing static folder in s3 behind cloudfront
export FLASKS3_BUCKET_NAME="static_s3_bucket_name"
export FLASKS3_CDN_DOMAIN="where_s3bucket_is_on.cloudfront.net"


#aws credentials
export AWS_ACCESS_KEY_ID ="aws_secret_access_key_id"
export AWS_SECRET_ACCESS_KEY ="aws_secret_access_key"
~~~~

#### Initialize the tables in your Postgres DB:

To initialize the tables in your database use:
```bash
python create_db.py
```
This will create the DB from scratch to use when you run the app.



#### To run the app use:


```bash
flask run
```

Input an ASIN and the corresponding Amazon listing will be scraped and its Review Data added to Postgres DB

#### To run the tests use:
```bash
pytest
```

#### To turn on storage of Output.html and/or product.json:

In amz_review_scraper/config.py there are 2 variables:
- **html_output_file_switch**
- **json_output_file_switch**

If you would like to switch on the output just change one or the other or both to = "y"

#### To Install additional packages:
After you install new packages use this code to lock the **Pipfile.lock**
```
pipenv lock --pre
```
This is because **Black** is a pre-release.  If you decide to remove **Black** as the linter of choice you will not have to do this when installing any new packages.
<a name="deployed_usage"/>
#  Deployed Usage


#### Upload Static files to s3 bucket and put them behind a cloudfront deployment. (for access from Lambda Function)

- Setup an s3 bucket and upload the whole static folder. It should be set to *Use this bucket to host a website*.
- Set bucket permissions (*this need more specific instructions*).
- Add your s3 bucket name to your .env file for **FLASKS3_BUCKET_NAME**
- Create a new cloudfront distribution using the s3 bucket you just created.
- In the cloudfront behaviors set /static/* to the bucket origin you just setup
- Cloudfront takes a while to deploy (20 minutes?), after it is deployed use the domain name field it populates (should look like d_random_stuff.cloudfront.net) and add it to your .env for **FLASKS3_CDN_DOMAIN**

## To launch as Lambda Function using Zappa:

Make sure you have your AWS credentials loaded using
```
awscli
```
You may want to set this up outside the environment. For help setting this up see the [awscli documentation](https://aws.amazon.com/cli/)
#### Initialize Zappa:


```
zappa init
```
[![asciicast](https://asciinema.org/a/225205.svg)](https://asciinema.org/a/225205)

Edit your **zappa_settings.json** file to add the exclude setting (shown below), since we are serving the static files from cloudfront/s3 bucket. Also add you environment variables here as the .env file will only help you locally so those same variables need to be in **zappa_settings.json** as well so that your Lambda function will have access to environment variables in the cloud.
### Important
- Add your **zappa_settings.json** to your **.gitignore** if you are using git for versioning since it contains sensitive info. You will also have another environment variable **ZAPPA** set to **True** which will set your environment to production when you are deployed with Zappa to Lambda.

### Example zappa_settings.json

```
{
    "dev": {
        "app_function": "run.app",                                              
        "aws_region": "us-east-2",                                              
        "profile_name": "default",                                              
        "project_name": "amz-review-scra",                                      
        "runtime" : "python3.6",                                                 
        "s3_bucket": "zappa-123443-zappa",
        "exclude": ["static", "test"],
        "aws_environment_variables" :
        {
            "FLASK_APP": "run.py",
            "FLASK_SECRET_KEY": "your_flask_secret_key",
            "FLASKS3_BUCKET_NAME": "static_s3_bucket_name",
            "FLASKS3_CDN_DOMAIN": "where_s3bucket_is_on.cloudfront.net",
            "http": "http://your_proxyservice",
            "https": "https://your_proxyservice",
            "DEV_SQLALCHEMY_DATABASE_URI": "postgresql://your_development_postgres_url_connection",
            "DEV_DEBUG" : "True",
            "DEV_LOGIN_BASE_URL":"http://127.0.0.1:5000",
            "TESTING_SQLALCHEMY_DATABASE_URI": "postgresql://postgres:@localhost:5432/travis_ci_test",
            "TESTING_DEBUG" : "True",
            "TESTING_TESTING" : "True",
            "TESTING_LOGIN_BASE_URL":"http://127.0.0.1:5000",
            "PROD_SQLALCHEMY_DATABASE_URI": "postgresql://your_production_postgres_url_connection",
            "PROD_LOGIN_BASE_URL":"https://your_custom_url.com",
            "ZAPPA": "True",
        },
        "use_precompiled_packages": true,
        "cors": true,
        "binary_support": false,
        }

}
```
#### Deploy to Lambda using Zappa:

```
zappa deploy
```
[![asciicast](https://asciinema.org/a/225207.svg)](https://asciinema.org/a/225207)

You can also initialize the DB using Zappa directly from the lambda function using: (**tip** don't forget the quotes):
```
zappa invoke <stage name> "create_db.db_init"
```
<a name="more"/>
### More things you should know
- Uses **psycopg2-binary** instead of psycopg2 because a future version of psycopg2 will involve a name change.  Using the binary version avoids the warning but may need to be changed at some point when SQLAlchemy updates its dependencies. I wrote this [Medium article](https://medium.com/@aswens0276/fixing-psycopg2-warning-for-flask-sqlalchemy-697e2430783e) with some more info on this.
<a name="contribute"/>
## How do you contribute to me?

In this project I am learning and practicing a number of skills, if you would like to comment on my code in places I could write better code, it would be much appreciated.

The project uses [Travis CI](https://travis-ci.org/) to automate testing and [Python Black](https://github.com/ambv/black) for Formatting and Automatic Format Checking
