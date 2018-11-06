# Valid ASINs are a combination of 10 Letters and Integers
# Not sure yet how to check is a seemingly valid ASIN is actually
# valid without first trying to scrape it
# example of seemingly valid ASIN = B011111111



def get_valid_asin():
    while True:
        asin = input("Please enter a vaild ASIN: ")
        if not len(asin) == 10:
            print("Invalid ASIN")
            continue
        else:
            return asin
