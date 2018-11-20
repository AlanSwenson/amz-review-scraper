product_json = {}
product_json["details"] = []


def find_attribute(soup, key, html_tag, attrs, *args, **kwargs):
    for tag in soup.findAll(html_tag, attrs=attrs, **kwargs):
        attribute = inner_attribute(tag, key, attrs=attrs, *args, **kwargs)
        if attribute is not None:
            return attribute
    return "None"


def inner_attribute(tag, key, attrs, *args, **kwargs):
    # For the Title, or Reviews Count Inner function
    if (
        attrs == {"id": "productTitle"}
        or attrs == {"id": "acrCustomerReviewText"}
        or attrs == {"class": "a-icon-alt"}
        or attrs == {"class": "a-list-item"}
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
