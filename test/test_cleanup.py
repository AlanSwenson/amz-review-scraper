import pytest
from amz_review_scraper.cleanup import review_count_cleanup


def test_review_count_cleanup():
    review1 = review_count_cleanup("32 customer reviews")
    review2 = review_count_cleanup("1,322 customer reviews")
    review3 = review_count_cleanup("0 customer reviews")
    review4 = review_count_cleanup(0)


    assert review1 == "32"
    assert review2 == "1322"
    assert review3 == "0"
    assert review4 == 0
