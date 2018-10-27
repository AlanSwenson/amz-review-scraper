import sys
import amzscraper as amazon

def main():
    asin = input("Please enter a vaild ASIN: ")
    url =  amazon.create_url(asin)
    amazon.scrape(url)
    print(url)
    sys.exit()

if __name__ == "__main__":
    main()
