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

    product_json["star-rating"] = find_attribute(
        soup, None, "i", attrs={"data-hook": "average-star-rating"}
    )

    product_json["details"] = find_attribute(
        soup, None, "div", attrs={"id": "feature-bullets"}
    )

    assert product_json["brand"] == "Sony"
    assert product_json["price"] == "$1298.00"
    assert (
        product_json["name"]
        == "Sony - FE 24-105mm F4 G OSS Standard Zoom Lens (SEL24105G)"
    )
    assert product_json["customer-reviews-count"] == "35 customer reviews"
    assert product_json["star-rating"] == "4.5 out of 5 stars"
    assert product_json["details"] == [
        "G-lens design with 4 aspherical and 3 ED glass (extra-low Dispersion) elements, for high corner-to-corner resolving power throughout the entire zoom range",
        "35 mm full-frame.Constant F4 maximum aperture maintains exposure and Depth of field throughout the zoom range",
        "9-blade circular aperture contributes to beautifuly de-focused bakgrounds",
        "Minimum focusing distance of just 125 feet provides close-up ability for an expansive range of expression",
        "In-the-box: Hood (ALC-SH152), Lens front cap (ALC-F77S), Lens rear cap (ALC-R1EM), Case",
    ]
