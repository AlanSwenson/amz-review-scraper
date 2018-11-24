import mock
import pytest
from amz_review_scraper.asin_validation import get_valid_asin


# @mock.patch("builtins.input", side_effect=trial_asins)
# @pytest.mark.parametrize("valid_asin", ["B07HJXVHSS"])
def is_valid_asin(trial_asins):
    with mock.patch("builtins.input", side_effect=trial_asins):
        return get_valid_asin()


def test_valid_asin():
    trial_asins = ["", "0", "-3", "abcdef8-", "&", "////", "B07HJXVHSS"]
    trial_asin = ["     b07HJXVHSS  "]

    assert is_valid_asin(trial_asins) == str("B07HJXVHSS")
    assert is_valid_asin(trial_asin) == str("B07HJXVHSS")
