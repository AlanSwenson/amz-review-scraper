def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, text, status_code):
            self.json_data = json_data
            self.text = text
            self.status_code = status_code

        def json(self):
            return self.json_data

    print("args: " + args[0])
    if args[0] == "https://www.amazon.com/gp/product/B111111111":
        return MockResponse({"key1": "value1"}, "sample text", 404)
    elif args[0] == "https://www.amazon.com/gp/product/B07HJXVHSS":
        return MockResponse({"key2": "value2"}, "sample text", 200)

    return MockResponse(None, 404)
