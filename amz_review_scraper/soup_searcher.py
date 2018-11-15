


def find_attribute(soup, key, html_tag, attrs):
    for tag in soup.findAll(html_tag, attrs=attrs):
        attribute = inner_attribute(tag, key, attrs)
        if attribute is not None:
            return attribute
    return "None"


def inner_attribute(tag, key, attrs):
    # For the Title, or Reviews Count Inner function
    if attrs == {"id": "productTitle"} or attrs == {"id": "acrCustomerReviewText"}:
        return tag.text.strip()
    # For Reviews Count Outer function
    elif attrs == {"id": "averageCustomerReviews_feature_div"}:
        return find_attribute(
            tag, None, "span", attrs={"id": "acrCustomerReviewText"}
        )
    else:
        if tag.get(key) is not None:
            return tag[key]
