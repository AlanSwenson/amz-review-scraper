Review Scraper for Amazon
===
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Build Status](https://travis-ci.org/AlanSwenson/amz-review-scraper.svg?branch=master)](https://travis-ci.org/AlanSwenson/amz-review-scraper) [![Coverage Status](https://coveralls.io/repos/github/AlanSwenson/amz-review-scraper/badge.svg)](https://coveralls.io/github/AlanSwenson/amz-review-scraper)

## What do I do?

This scrapes Amazon recent reviews for specified products on and stores them in a Postgres DB

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
## How do you use me?


### To run the app use:
```bash
python app.py
```

Input an ASIN and the corresponding Amazon listing will be scraped and its Review Data added to Postgres DB

### To run the tests use:
```bash
pytest
```

## How do you contribute to me?

In this project I am learning and practicing a number of skills, if you would like to comment on my code in places I could write better code, it would be much appreciated.

The project uses [Travis CI](https://travis-ci.org/) to automate testing and [Python Black](https://github.com/ambv/black) for Formatting and Automatic Format Checking
