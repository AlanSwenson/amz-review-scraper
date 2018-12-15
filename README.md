Review Scraper for Amazon
===
![Programming language: python](https://img.shields.io/badge/python-3.6-blue.svg) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Build Status](https://travis-ci.org/AlanSwenson/amz-review-scraper.svg?branch=master)](https://travis-ci.org/AlanSwenson/amz-review-scraper) [![Coverage Status](https://coveralls.io/repos/github/AlanSwenson/amz-review-scraper/badge.svg)](https://coveralls.io/github/AlanSwenson/amz-review-scraper)





## What do I do?

This project scrapes Amazon listings for recent reviews of specified products (ASIN) and stores them in a Postgres DB

##### Future Features

- Emails users when their subscribed ASIN has a new review
- Custom routes domain.com/ASIN for displaying the reviews and stats related to each ASIN

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


## Setup

#### Create an empty PostreSQL database
This project uses Postgres as it's database of choice. Either locally or in the cloud, create a new, empty Postres DB. Use the credentials from your new DB to complete the .env file below.  In this project there is a local DB setup for **development** and an RDS DB setup for **production**. You need at least 1 setup but not both if you are not into that sort of thing.

#### Upload Static files to s3 bucket and put them behind a cloudfront deployment. (for use as Lambda Function)

- Setup an s3 bucket and upload the whole static folder. It should be set to *Use this bucket to host a website*.
- Set bucket permissions (*this need more specific instructions*).
- Add your s3 bucket name to your .env file for **FLASKS3_BUCKET_NAME**
- Create a new cloudfront distribution using the s3 bucket you just created.
- In the cloudfront behaviors set /static/* to the bucket origin you just setup
- Cloudfront takes a while to deploy (20 minutes?), after it is deployed use the domain name field it populates (should look like d_random_stuff.cloudfront.net) and add it to your .env for **FLASKS3_CDN_DOMAIN**


#### Set up a .env file
~~~~
#db variables

#development
export DEV_POSTGRES_URL="localhost:5432"
export DEV_POSTGRES_USER="Change Me"
export DEV_POSTGRES_PW="Change Me"
export DEV_POSTGRES_DB="Change Me"

#production
export PROD_POSTGRES_URL="Change Me:5432"
export PROD_POSTGRES_USER="Change Me"
export PROD_POSTGRES_PW="Change Me"
export PROD_POSTGRES_DB="Change Me"

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

#### To change the use of production or development DB:

In amz_review_scraper/config.py change the variable:

- **env_setting**

can be *production* or *development*


#### To Install additional packages:
After you install new packages use this code to lock the **Pipfile.lock**
```
pipenv lock --pre
```
This is because **Black** is a pre-release.  If you decide to remove **Black** as the linter of choice you will not have to do this when installing any new packages.

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
[![asciicast](https://asciinema.org/a/gtxtUWsF0JdFBusOHA34EQTRS.svg)](https://asciinema.org/a/gtxtUWsF0JdFBusOHA34EQTRS)

Edit your **zappa_settings.json** file to add the exclude setting, since we are serving the static files from cloudfront/s3 bucket. Also add you environment variables here as the .env file will only help you locally so those same variables need to be in **zappa_settings.json** as well so that your Lambda function will have access to enviroment variables in the cloud.
### Important
- Add your **zappa_settings.json** to your **.gitignore** if you are using git for versioning since it contains sensitive info.

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
        "environment_variables": {
            "your_key": "your_value"
        }
        }

}
```
#### Deploy to Lambda using Zappa:

```
zappa deploy
```
TODO: *add zappa deploy video*

You can also initialize the DB using zappa directly from the lambda function using:
```
zappa invoke <stage name> "create_db.db_init"
```
### More things you should know
- Uses **psycopg2-binary** instead of psycopg2 because a future version of psycopg2 will involve a name change.  Using the binary version avoids the warning but may need to be changed at some point when SQLAlchemy updates its dependencies.

## How do you contribute to me?

In this project I am learning and practicing a number of skills, if you would like to comment on my code in places I could write better code, it would be much appreciated.

The project uses [Travis CI](https://travis-ci.org/) to automate testing and [Python Black](https://github.com/ambv/black) for Formatting and Automatic Format Checking
