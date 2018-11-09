import mock
import pytest
from amz_review_scraper.asin_validation import get_valid_asin

@pytest.mark.parametrize('valid_asin', ['B07HJXVHSS'])
def test_valid_asin(valid_asin):
    trial_asins = ["", "0", "-3", "abcdef8-", "&", "////", valid_asin]
    with mock.patch('builtins.input', side_effect=trial_asins):
        assert get_valid_asin() == str(valid_asin)
