product_json = {}


def find_attribute(soup, key, html_tag, attrs, *args, **kwargs):

    product_json["short-reviews"] = []
    product_json["long-reviews"] = []
    for tag in soup.findAll(html_tag, attrs=attrs, **kwargs):

        attribute = inner_attribute(tag, key, attrs=attrs, *args, **kwargs)
        if attrs == {
            "class": "a-size-base a-link-normal review-title a-color-base a-text-bold"
        }:
            tag = tag.text.strip()
            product_json["short-reviews"].append(tag)
            continue
        if attrs == {"data-hook": "review-collapsed"}:
            tag = tag.text.strip()
            product_json["long-reviews"].append(tag)
            continue

        if attribute is not None:
            return attribute
    if product_json["short-reviews"] and product_json["short-reviews"] != []:
        return product_json["short-reviews"]
    if product_json["long-reviews"] and product_json["long-reviews"] != []:
        return product_json["long-reviews"]
    return None


def inner_attribute(tag, key, attrs, *args, **kwargs):
    # For the Title, or Reviews Count Inner function
    if (
        # Title
        attrs == {"id": "productTitle"}
        # Reviews Count
        or attrs == {"id": "acrCustomerReviewText"}
        or attrs == {"class": "a-icon-alt"}
        or attrs == {"class": "a-list-item"}
        # Short Reviews
        or attrs
        == {"class": "a-size-base a-link-normal review-title a-color-base a-text-bold"}
        # Long Reviews
        or attrs == {"data-hook": "review-collapsed"}
    ):
        return tag.text.strip()

    # Reviews Count Inner Function
    elif attrs == {"id": "averageCustomerReviews_feature_div"}:
        return find_attribute(tag, None, "span", attrs={"id": "acrCustomerReviewText"})

    # Star Rating Inner Function
    elif attrs == {"data-hook": "average-star-rating"}:
        return find_attribute(tag, None, "span", attrs={"class": "a-icon-alt"})

    # Detail Bullets First Inner Function
    elif attrs == {"id": "feature-bullets"}:
        return find_attribute(
            tag,
            None,
            "ul",
            attrs={"class": "a-unordered-list a-vertical a-spacing-none"},
        )

    # Detail Bullets Second Inner Function
    elif attrs == {"class": "a-unordered-list a-vertical a-spacing-none"}:
        product_json["details"] = []
        for li_tag in tag.findAll("li", id=False):
            temp_value = find_attribute(
                li_tag,
                None,
                "span",
                attrs={"class": "a-list-item"},
                text=True,
                recursive=False,
                id=False,
            )
            temp_value = temp_value.replace("\n", " ")
            product_json["details"].append(temp_value)
        return product_json["details"]

    # Brand
    else:
        if tag.get(key) is not None:
            return tag[key]
