#!/usr/bin/python
# -*- coding: utf-8 -*-
import json

import model_functions
import models.item as item
import models.review as review
from soup_searcher import find_attribute
import cleanup
from config import html_output_file_switch, json_output_file_switch


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

    try:
        scraped_item = item.Item(
            name=product_json["name"], customer_reviews_count=review_count, asin=asin
        )
        # TODO: think of a better name than item_exists
        item_exists = scraped_item.check()
        if item_exists == None:
            scraped_item.save()
        else:
            scraped_item.update_last_scraped()
            # scraped_item = item_exists

    except Exception as e:
        model_functions.db_error("Item", e)
        raise

    # This block of code will help extract the long reviews of the product
    product_json["long-reviews"] = []
    for divs in soup.findAll("div", attrs={"data-hook": "review-collapsed"}):
        long_review = divs.text.strip()
        try:
            scraped_review = review.Review(
                review=long_review, asin=asin, owner=scraped_item
            )
            review_exists = scraped_review.check()
            if review_exists == None:
                scraped_review.save()
            else:
                pass
        except Exception as e:
            model_functions.db_error("Review", e)
            raise
        product_json["long-reviews"].append(long_review)
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
