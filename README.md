Review Scraper for Amazon
===
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black) [![Build Status](https://travis-ci.org/AlanSwenson/amz-review-scraper.svg?branch=master)](https://travis-ci.org/AlanSwenson/amz-review-scraper)

## What do I do?

This scrapes Amazon recent reviews for specified products on and stores them in a Postgres DB

## Install

This project uses [pipenv](https://github.com/pypa/pipenv) for virtual environments

```bash
pip install pipenv
pipenv sync
pipenv shell
```
## How do you use me?

### To run the app use:
```bash
python app.py
```

### To run the tests use:
```bash
pytest
```


Input an ASIN and the corresponding Amazon listing will be scraped and its Review Data added to Postgres DB


## How do you contribute to me?

In this project I am learning and practicing a number of skills, if you would like to comment on my code in places I could write better code, it would be much appreciated.

The project uses [Travis CI](https://travis-ci.org/) to automate testing and [Python Black](https://github.com/pytest-dev/pytest) for Formatting and Automatic Format Checking
