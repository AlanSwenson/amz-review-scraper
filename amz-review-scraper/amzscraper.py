#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import bs4
import lxml
import ssl
import json
from config import proxies
from app import db

# For ignoring SSL certificate errors

#ctx = ssl.create_default_context()
#ctx.check_hostname = False
#ctx.verify_mode = ssl.CERT_NONE

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}

# This is a great little method, it takes some input, delivers some ouput.
# But why not make it even simpler!
# no reason to assign a local variable, only to just return it a second later, just inline that return!
#
# And I'm not going to tell you how to live you life, but I feel like the cool kids are using f strings
# these days. There are also other reasons I don't want to get into, because the details aren't important now!
#
# def create_url(asin):
#     return f"https://www.amazon.com/gp/product/{asin}"
#
def create_url(asin):

    url = ("https://www.amazon.com/gp/product/" + asin)
    return url

def scrape(url, asin):
    # You use this html variable name also below after prettifying. Which looks to be the same object as original,
    # just transformed some. While truthfully this is not offensive at all in this context, I say in when starting
    # out to code, to just avoid this practice, which is often called variable shadowing.
    #
    # On one hand there are perfect valid use cases for it, and on the other many langauges bane the practice altogether.
    # I think it has a prone to cause really annoying issues to debug early on, and the exceptions are rare,
    # and worth an interesting conversation.
    #
    # It also makes you stretch the naming muscles harder!
    # Like somethings in this case, you might change the first name to be something like raw_html
    # or you could go the other way and rename the html to something like utf8_html prettified_html.
    # or change both!
    #
    # Last thing is when I look for the next occurance of html, it's on line 144!
    # 96 lines away!
    # That is much to far away for a variable to be declared before it's use.
    html = requests.get(url, headers=header, proxies=proxies)
    soup = bs4.BeautifulSoup(html.text, 'lxml')
    html = soup.prettify('utf-8')
    product_json = {}
    review_count = 0

    # This block of code will help extract the Brand of the item

    for divs in soup.findAll('div', attrs={'class': 'a-box-group'}):
        try:
            product_json['brand'] = divs['data-brand']
            break
        except:
            pass

    # This block of code will help extract the Prodcut Title of the item

    for spans in soup.findAll('span', attrs={'id': 'productTitle'}):
        name_of_product = spans.text.strip()
        product_json['name'] = name_of_product
        break

    # This block of code will help extract the price of the item in dollars

    for divs in soup.findAll('div'):
        try:
            price = str(divs['data-asin-price'])
            product_json['price'] = '$' + price
            break
        except:
            pass

    # This block of code will help extract the image of the item in dollars

    for divs in soup.findAll('div', attrs={'id': 'rwImages_hidden'}):
        for img_tag in divs.findAll('img', attrs={'style': 'display:none;'
                                    }):
            product_json['img-url'] = img_tag['src']
            break

    # This block of code will help extract the average star rating of the product

    for i_tags in soup.findAll('i',
                               attrs={'data-hook': 'average-star-rating'}):
        for spans in i_tags.findAll('span', attrs={'class': 'a-icon-alt'}):
            product_json['star-rating'] = spans.text.strip()
            break

    # This block of code will help extract the number of customer reviews of the product
    # the first line is needed to grab the correct div with the total reviews
    for divs in soup.findAll('div', attrs={'id': 'averageCustomerReviews_feature_div'}):
        for spans in divs.findAll('span', attrs={'id': 'acrCustomerReviewText'
                                  }):
            if spans.text:
                print(spans.text)
                review_count = spans.text.strip()
                product_json['customer-reviews-count'] = review_count
                break

    # This block of code will help extract top specifications and details of the product

    product_json['details'] = []
    for ul_tags in soup.findAll('ul',
                                attrs={'class': 'a-unordered-list a-vertical a-spacing-none'
                                }):
        for li_tags in ul_tags.findAll('li'):
            for spans in li_tags.findAll('span',
                    attrs={'class': 'a-list-item'}, text=True,
                    recursive=False):
                product_json['details'].append(spans.text.strip())

    # This block of code will help extract the short reviews of the product

    product_json['short-reviews'] = []
    for a_tags in soup.findAll('a',
                               attrs={'class': 'a-size-base a-link-normal review-title a-color-base a-text-bold'
                               }):
        short_review = a_tags.text.strip()

        #data = Reviews(asin=asin, review=short_review)
        #ds.session.add(data)
        product_json['short-reviews'].append(short_review)

    # This block of code will help extract the long reviews of the product

    product_json['long-reviews'] = []
    for divs in soup.findAll('div', attrs={'data-hook': 'review-collapsed'
                             }):
        long_review = divs.text.strip()




        product_json['long-reviews'].append(long_review)

    # Saving the scraped html file

    with open('output_file.html', 'wb') as file:
        file.write(html)

    # Saving the scraped data in json format

    with open('product.json', 'w') as outfile:
        json.dump(product_json, outfile, indent=4)
    print ('----------Extraction of data is complete. Check json file.----------')

    # Class for returning the Item back for database storage
    class Result:
        def __init__(self, name, count):
            self.name = name
            try:
                self.count = count.replace(',','')
                self.count = self.count.replace(' customer reviews','')
            except:
                self.count = count

    #reg = Items(name_of_product, review_count)
    #reg = Items(name=Result.name, customer_reviews_count=result.count, asin=asin)

    #db.session.add(reg)
    #db.session.commit()
    return Result(name_of_product, review_count)
