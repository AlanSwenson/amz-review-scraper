#!/usr/bin/python
# -*- coding: utf-8 -*-
import ssl
import json
import models
from soup_searcher import find_attribute
import cleanup


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

    # This block of code will help extract the average star rating of the product

    for i_tags in soup.findAll("i", attrs={"data-hook": "average-star-rating"}):
        for spans in i_tags.findAll("span", attrs={"class": "a-icon-alt"}):
            product_json["star-rating"] = spans.text.strip()
            break

    # This block of code will help extract top specifications and details of the product

    product_json["details"] = []
    for ul_tags in soup.findAll(
        "ul", attrs={"class": "a-unordered-list a-vertical a-spacing-none"}
    ):
        for li_tags in ul_tags.findAll("li"):
            for spans in li_tags.findAll(
                "span", attrs={"class": "a-list-item"}, text=True, recursive=False
            ):
                product_json["details"].append(spans.text.strip())

    # This block of code will help extract the short reviews of the product

    product_json["short-reviews"] = []
    for a_tags in soup.findAll(
        "a",
        attrs={
            "class": "a-size-base a-link-normal review-title a-color-base a-text-bold"
        },
    ):
        short_review = a_tags.text.strip()

        product_json["short-reviews"].append(short_review)

    # Saving the scraped html file
    # pretty_html = soup.prettify('utf-8')
    # with open('output_file.html', 'wb') as file:
    #    file.write(pretty_html)

    # Saving the scraped data in json format

    with open("product.json", "w") as outfile:
        json.dump(product_json, outfile, indent=4)
        print("----------Extraction of data is complete. Check json file.----------")

    try:
        scraped_item = models.Item(
            name=product_json["name"], customer_reviews_count=review_count, asin=asin
        )
        # TODO: think of a better name than item_exists
        item_exists = scraped_item.check()
        if item_exists == None:
            scraped_item.save()
        else:
            scraped_item = item_exists

    except Exception as e:
        models.db_error("Item", e)
        raise

    # This block of code will help extract the long reviews of the product
    product_json["long-reviews"] = []
    for divs in soup.findAll("div", attrs={"data-hook": "review-collapsed"}):
        long_review = divs.text.strip()
        try:
            scraped_review = models.Review(
                review=long_review, asin=asin, owner=scraped_item
            )
            review_exists = scraped_review.check()
            if review_exists == None:
                scraped_review.save()
            else:
                pass
        except Exception as e:
            models.db_error("Review", e)
            raise
        product_json["long-reviews"].append(long_review)
        models.save_to_db()
    return
