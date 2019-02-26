#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from flask import redirect, url_for

import amz_review_scraper.model_functions as model_functions
import amz_review_scraper.models.item as item
import amz_review_scraper.models.review as review
import amz_review_scraper.models.user as user_methods
from amz_review_scraper.soup_searcher import find_attribute
import amz_review_scraper.cleanup as cleanup
from amz_review_scraper.config import html_output_file_switch, json_output_file_switch


def scrape(soup, asin):

    product_json = {}
    product_json["customer-reviews-count"] = 0

    product_json["brand"] = find_attribute(
        soup, "data-brand", "div", attrs={"class": "a-box-group"}
    )

    product_json["price"] = "$" + str(
        find_attribute(soup, "data-asin-price", "div", attrs={})
    )

    product_json["name"] = find_attribute(
        soup, None, "span", attrs={"id": "productTitle"}
    )

    product_json["customer-reviews-count"] = find_attribute(
        soup, None, "div", attrs={"id": "averageCustomerReviews_feature_div"}
    )

    review_count = cleanup.review_count_cleanup(product_json["customer-reviews-count"])

    product_json["star-rating"] = find_attribute(
        soup, None, "i", attrs={"data-hook": "average-star-rating"}
    )

    product_json["details"] = find_attribute(
        soup, None, "div", attrs={"id": "feature-bullets"}
    )

    product_json["short-reviews"] = find_attribute(
        soup,
        None,
        "a",
        attrs={
            "class": "a-size-base a-link-normal review-title a-color-base a-text-bold"
        },
    )

    product_json["long-reviews"] = find_attribute(
        soup, None, "div", attrs={"data-hook": "review-collapsed"}
    )

    # saving an item to DB
    try:
        # TODO It is possible to use the JWT library to get the user
        user = user_methods.get_current_user()
        scraped_item = item.Item(
            name=product_json["name"], customer_reviews_count=review_count, asin=asin
        )

        scraped_item = scraped_item.add(user=user)

    except Exception as e:
        model_functions.db_error("Item", e)
        raise

    # saving reviews for the item to db
    for long_review in product_json["long-reviews"]:
        try:
            review_exists = review.get_results(asin=asin, review=long_review)
            if review_exists is None:
                scraped_review = review.Review(
                    review=long_review, asin=asin, owner=scraped_item
                )
                review.save(scraped_review)
            else:
                print("Review already exists")
        except Exception as e:
            model_functions.db_error("Review", e)
            raise
    # commit everything to DB
    model_functions.save_to_db()

    # Saving the scraped html file
    if html_output_file_switch == "y":
        pretty_html = soup.prettify("utf-8")
        with open("output_file.html", "wb") as file:
            file.write(pretty_html)

    # Saving the scraped data in json format
    if json_output_file_switch == "y":
        with open("product.json", "w") as outfile:
            json.dump(product_json, outfile, indent=4)
            print(
                "----------Extraction of data is complete. Check json file.----------"
            )

    return
