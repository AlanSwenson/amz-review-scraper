


def find_attribute(soup, key, html_tag, attrs):
    product_container = {}
    for tag in soup.findAll(html_tag, attrs=attrs):
        # For the Title, or Reviews Count inner function
        if attrs == {"id": "productTitle"} or attrs == {"id": "acrCustomerReviewText"}:
            return tag.text.strip()
        # For Reviews Count Outer function
        elif attrs == {"id": "averageCustomerReviews_feature_div"}:
            return find_attribute(
                tag, None, "span", attrs={"id": "acrCustomerReviewText"}
            )
        else:
            try:
                return tag[key]
            except:
                pass
    return "None"
