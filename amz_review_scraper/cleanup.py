

def review_count_cleanup(reviews):
    try:
        reviews = reviews.replace(",", "")
        reviews = reviews.replace(" customer reviews", "")
    except:
        pass
    return reviews
