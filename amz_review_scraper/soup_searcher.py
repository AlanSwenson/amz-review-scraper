
def find_attribute(soup, key, html_tag, attrs):
    for divs in soup.findAll(html_tag, attrs=attrs):
        if html_tag == "span":
            return divs.text.strip()
        else:
            try:
                return divs[key]
            except:
                pass
    return "None"
