def mocked_env_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, name):
            self.name = name

    if args[0] == "POSTGRES_URL":
        return MockResponse("fake_postgres_url")
    elif args[0] == "POSTGRES_USER":
        return MockResponse("fake_postgres_user")
    elif args[0] == "POSTGRES_PW":
        return MockResponse("fake_postgres_pw")
    elif args[0] == "POSTGRES_DB":
        return MockResponse("fake_postgres_db")
