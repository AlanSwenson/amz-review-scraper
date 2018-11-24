import mock
import pytest

from amz_review_scraper.config import get_env_variable
from test.support.mocked_env import mocked_env_get


@mock.patch("os.environ.get")
def test_get_env_variable(self):
    self.side_effect = mocked_env_get
    POSTGRES_URL = get_env_variable("POSTGRES_URL")
    POSTGRES_USER = get_env_variable("POSTGRES_USER")
    POSTGRES_PW = get_env_variable("POSTGRES_PW")
    POSTGRES_DB = get_env_variable("POSTGRES_DB")
    INVALID_ENV_VAR = get_env_variable("INVLAID")

    assert POSTGRES_URL.name == "fake_postgres_url"
    assert POSTGRES_USER.name == "fake_postgres_user"
    assert POSTGRES_PW.name == "fake_postgres_pw"
    assert POSTGRES_DB.name == "fake_postgres_db"
    assert INVALID_ENV_VAR == None
