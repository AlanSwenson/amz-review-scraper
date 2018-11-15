import os

import pytest
import codecs
import bs4

from amz_review_scraper.soup_searcher import find_attribute


my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "materials/sample_output_file.html")

raw_html = codecs.open(path, "r")
soup = bs4.BeautifulSoup(raw_html, "lxml")
product_json = {}


def test_find_attribute():
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

    assert product_json["brand"] == "Sony"
    assert product_json["price"] == "$1298.00"
    assert (
        product_json["name"]
        == "Sony - FE 24-105mm F4 G OSS Standard Zoom Lens (SEL24105G)"
    )
    assert product_json["customer-reviews-count"] == "32 customer reviews"
