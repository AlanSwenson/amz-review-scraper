#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import bs4
import lxml
import ssl
import json
from config import proxies
from app import db
import models

header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0'}


def scrape(url, asin):
    #print(type(proxies))
    print("Asin " + asin)
    raw_html = requests.get(url, headers=header, proxies=proxies)
    soup = bs4.BeautifulSoup(raw_html.text, 'lxml')
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



    # Saving the scraped html file
    # pretty_html = soup.prettify('utf-8')
    # with open('output_file.html', 'wb') as file:
    #    file.write(pretty_html)

    # Saving the scraped data in json format

    #with open('product.json', 'w') as outfile:
    #    json.dump(product_json, outfile, indent=4)
    #print ('----------Extraction of data is complete. Check json file.----------')

    # Class for returning the Item back for database storage
    class Result:
        def __init__(self, name, reviews):
            self.name = name
            try:
                self.reviews = reviews.replace(',','')
                self.reviews = self.reviews.replace(' customer reviews','')
                # & mess up the save to DB -- this doesn't work???
                # self.name = name.replace('&','and')
            except:
                self.reviews = reviews


    result = Result(name_of_product, review_count)

    try:
        scraped_item = models.Items( name=result.name,
                                    customer_reviews_count=result.reviews,
                                    asin=asin)

        db.session.add(scraped_item)

    except:
        print('An Error Occured While Saving Item to DB')
        db.session.rollback()
        raise


    product_json['long-reviews'] = []
    for divs in soup.findAll('div', attrs={'data-hook': 'review-collapsed'
                             }):
        long_review = divs.text.strip()
        try:
            scraped_review = models.Review(  review=long_review,
                                            asin=asin, owner=scraped_item)

            db.session.add(scraped_review)
        except:
            print('An Error Occured While Adding a Review')
            raise
        product_json['long-reviews'].append(long_review)

    try:
        db.session.commit()
    except:
        print('An Error Occured While Saving to DB')
        db.session.rollback()
        raise
    finally:
        db.session.close()

    return
