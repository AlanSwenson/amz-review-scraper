
# Rule of 3

# DRY is a mantra you will hear often, and you be repeating it to yourself:
#   Don't Repeat Yourself
#   Don't Repeat Yourself
#   Don't Repeat Yourself
#
# If you find yourself writing the same code you then you should figure out how to extract that code
# into an abstraction. This usually means making a new method, or class, or many method classes and methods!
#
# However, you will start hearing another phrase as you continue on your programming journey.
# And after getting burnt on it a couple hundred times, you too will will jump to throw it in any
# conversation about refactoring a newer system: Pre-Mature Optimization is the Root of All Evil.
# Said by a name that will come up often in talking about programming: https://en.wikipedia.org/wiki/Donald_Knuth
#
# How this often manifests itself, is you see two pieces of code that look similar, so you extract them into
# a method and give it a name, and when you name it you give it a name that matches it's concept now, but
# won't as the application evolves. This leads to a cascade of naming problems, that affects the evolution
# of whole application.
#
# So it's all about a balance.
# This is where the rule of 3 comes in. When you find code that you have repeated 3 times then extract it.
# So don't worry about Drying everything up, until you find yourself doing it for the third time.

# This code all looked similiar, so heres kinda some general approach to refactoring it.
    # # This block of code will help extract the Brand of the item

    # for divs in soup.findAll('div', attrs={'class': 'a-box-group'}):
    #     try:
    #         product_json['brand'] = divs['data-brand']
    #         break
    #     except:
    #         pass

    # # This block of code will help extract the Prodcut Title of the item

    # for spans in soup.findAll('span', attrs={'id': 'productTitle'}):
    #     name_of_product = spans.text.strip()
    #     product_json['name'] = name_of_product
    #     break

    # # This block of code will help extract the price of the item in dollars

    # for divs in soup.findAll('div'):
    #     try:
    #         price = str(divs['data-asin-price'])
    #         product_json['price'] = '$' + price
    #         break
    #     except:
    #         pass

# I just separated each block into its own method
# I also switched to using the next() command
# This is just a more pythonista way to find the first occurance
# Which seems to be what these are doing.
#
# Then you start see the similaries of the methods
# and how they could be refactored further
# def find_brand(soup):
#     return next((div["data-brand"]
#           for div in soup.findAll('div', attrs={'class': 'a-box-group'})
#           if div["data-brand"] is not null))


# def find_product_title(soup):
#     return next((div["name"].text.strip()
#           for spans in soup.findAll('span', attrs={'id': 'productTitle'})
#           if div["name"] is not null))


# def find_price(soup):
#     return next(('$' + str(div["data-asin-price"])
#           for div in soup.findAll('div'):
#           if div["data-asin-price"] is not null))


# def scrape(url, asin):
#     product_json['brand'] = find_brands(soup)
#     product_json['name'] = find_product_title(soup)
#     product_json['price'] = find_product_title(soup)

# Then I notice What makes each differently, and one of things I notice is the formatting of the strings.
# and I then defer to the single-responsibility principal, a method should do 1 thing!
# and this is finding and formatting, so I want to move the formatting to the outside,
# and then extract out the different values into variables


def find_attribute(soup, key, html_tag, attrs = {}):
    return next((div[key]
          for div in soup.findAll(html_tag, attrs=attrs):
          if div[key] is not null))

def scrape(url, asin):
    # ...

    product_json['brand'] = find_attribute(soup, "data-brand", "div", attrs = {'class': 'a-box-group'})
    product_json['name'] = find_attribute(soup, "name", "span", attrs = {'id': 'productTitle'}).text.strip()
    product_json['price'] = "$" + str(find_attribute(soup, "data-asin-price", "div"))

    # ...
