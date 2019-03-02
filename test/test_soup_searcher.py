"""Tests for soup_searcher.py"""

import os

import codecs
import bs4

from amz_review_scraper.soup_searcher import find_attribute

my_path = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(my_path, "materials/sample_output_file.html")

raw_html = codecs.open(path, "r")
soup = bs4.BeautifulSoup(raw_html, "lxml")
product_json = {}


def test_find_attribute():
    """Testing find_attribute function from soup_searcher"""
    product_json["brand"] = find_attribute(
        soup, "data-brand", "div", attrs={"class": "a-box-group"}
    )

    product_json["price"] = "$" + str(
        find_attribute(soup, "data-asin-price", "div", attrs={})
    )

    product_json["name"] = find_attribute(
        soup, None, "span", attrs={"id": "productTitle"}
    )

    product_json["customer-reviews-count"] = find_attribute(
        soup, None, "div", attrs={"id": "averageCustomerReviews_feature_div"}
    )

    product_json["star-rating"] = find_attribute(
        soup, None, "i", attrs={"data-hook": "average-star-rating"}
    )

    product_json["details"] = find_attribute(
        soup, None, "div", attrs={"id": "feature-bullets"}
    )

    product_json["short-reviews"] = find_attribute(
        soup,
        None,
        "a",
        attrs={
            "class": "a-size-base a-link-normal review-title a-color-base a-text-bold"
        },
    )
    product_json["tag-that-doesnt-exist"] = find_attribute(
        soup, "tag-that-doesnt-exist", "tag-that-doesnt-exist", attrs={}
    )
    product_json["long-reviews"] = find_attribute(
        soup, None, "div", attrs={"data-hook": "review-collapsed"}
    )
    assert product_json["brand"] == "Sony"
    assert product_json["price"] == "$1298.00"
    assert (
        product_json["name"]
        == "Sony - FE 24-105mm F4 G OSS Standard Zoom Lens (SEL24105G)"
    )
    assert product_json["customer-reviews-count"] == "35 customer reviews"
    assert product_json["star-rating"] == "4.5 out of 5 stars"
    assert product_json["details"] == [
        "G-lens design with 4 aspherical and 3 ED glass (extra-low Dispersion) elements, for high corner-to-corner resolving power throughout the entire zoom range",
        "35 mm full-frame.Constant F4 maximum aperture maintains exposure and Depth of field throughout the zoom range",
        "9-blade circular aperture contributes to beautifuly de-focused bakgrounds",
        "Minimum focusing distance of just 125 feet provides close-up ability for an expansive range of expression",
        "In-the-box: Hood (ALC-SH152), Lens front cap (ALC-F77S), Lens rear cap (ALC-R1EM), Case",
    ]
    assert product_json["short-reviews"] == [
        "Simple Comparison of 24-70/2.8 GM and 24-105/4 - Both are amazing, but its all about the comfort",
        "Some barrel distortion at 24mm but easily corrected. Good colors and fantastic bokeh with 9 ...",
        "Won't let you down.",
        "Sharp, not too heavy, fast focus, great focal range",
        "One of the BEST of current market zooms, regardless of price or manufacturer.",
        "Sharp, versatile and lightweight.",
        "Beats Zeiss 24-70",
        "Five Stars",
    ]
    assert product_json["tag-that-doesnt-exist"] is None

    assert product_json["long-reviews"] == [
        "I purchased the 24-70/2.8 GM lens first.  Its heavy.  Very Heavy.  There is no balance with the body, and it strains my wrist to hold it.  I purchased the Peak Design Clutch and that made a world of difference on the positive side.  When getting ready for a family site-seeing trip, I found the camera with attached lens would not fit in my 5L camera bag.  the barrel and length of the lens was too big.  I put the camera and lens in a backpack, and off we went.  By the end of the day, my back was sore and my arms tired.  It is that heavy (or rather, it is that unbalanced as it strained my wrist).  I only took a few portait shots of my family, and I noticed that I was usually at F4 or smaller.  To get to 2.8, I had to manually over-ride the program setting.  The photos are amazing, but the camera was so heavy that I dred using it the following day.  I used my iPhone instead.  This is when I learned that there is a reason why Sony offers a 24-70/2.8 GM, and a 24-105/4.  Its all about the trade-off between portability and shallow depth of field.\n                      \n\n                      I purchased the 24-105/4 for the purpose of being a site-seeing lens.  It is much lighter, and much shorter, and a smaller diameter ... it travels a lot easier by using a smaller camera bag.  The weight is much more balanced, and easier on my wrist providing a lot more comfort for all-day shooting.  The extra reach from the telephoto is also nice for site-seeing as many items in museums are beyond reach of a 70mm lens, but I still want that 24mm for family group shots.\n                      \n\n                      With this learning, here is what I am doing.  The 24-70/2.8 is my portrait lens, and it will be used when i am shooting closer subjects in a darker setting of low duration.  The 24-105/4 is my travel and site seeing lens.  Both have a purpose.\n                      \n\n                      But now that I said all of this, consider the following - I also have a 85/1.4 GM that can easily replace the 24-70/2.8 for potraits, and I have the 18-35/2.8 GM lens that can replace the 24-70/2.8 GM for wide angle nature photography.  In some respects, the 24-70/2.8GM lens is no longer needed and can be sold.  If I was starting from scratch, I would not have purchased the 24-70/2.8 GM.\n                      \n\n                      One last comment - I do have the 70-200/4 lens, and love it for its lighter weight and better balance than the 70-200/2.8 GM.  I realize that I loose an f-stop, but I doubt I would use a lens that is too hard on my wrist.\n                      \n\n                      In summary, the GM lenses are the considered the best lenses.  They come at a higher price, higher weight, and longer length that reduce their portability and usability.  Before thinking that only the best lens will do for you, think about ergonomics and the strength of your wrist.  You might find that the best lens is the one that best serves your personal needs.",
        "Don't listen to anyone playing down this lens with the exception of price!  I'm a pro and have had 30 years of lens sampling.  This lens is SHARY wide open all the way up.  Some barrel distortion at 24mm but easily corrected.  Good colors and fantastic bokeh with 9 blades.  IS works fantastic on the new A7R3 and the focus is very fast.  Weight is a non issue and the size is very manageable considering the zoom range.  Great for portraits as well.  Heres a SOOC .jpeg",
        "Wow, this lens really delivers. Versatile zoom range, fast autofocus, great depth of field at F4, sharp enough for nearly every kind of photography. I'm not a pixel counter nor a technician. But I've shot enough photos in my life to know that this lens is outstanding.",
        "This is quite a step up from the 24-70 f4. It is sharp throughout the entire focal range and focus is fast. The weight of this lens is at the upper limit of what I want to carry all day and much better feeling in hand than the 24-70 f2.8 which feels unpleasantly heavy on a A9. It is easy to understand why this lens has been in short supply for so long.",
        "Just flat out excellent across the board.\n                      \n\n                      Better than the shorter range 24-70/2.8, and almost half the price.\n                      \n\n                      I don't understand this insane lurching towards faster and faster, heavier and much more expensive glass when most of us who used to shoot Kodachrome 25 or 64 now start out the door at ISO 800-1,600 and don't think twice about it because the digital dystems are so clean and sharp.\n                      \n\n                      Small sharp, less expensive zooms are terrific by me.\n                      \n                      I don't need to be the my-lens-is-bigger-than-your-lens guy.",
        "This lens is absurdly sharp and versatile. Don't need anything else to carry during my travels.",
        "So, I swapped my SEL2470Z to this 25105G, mainly for better reach. I expected to have slight loss of absolute image quality, but I was completely proven wrong about that. This lens is as good if not even better than the Zeiss, likely due to the OSS.\n                      \n                      Now, I use it on my A7Riii body which also has nobody stabilization. Even in low light the shots turn out beautiful.\n                      \n                      Color rendering as well on this lens is magnificent. If I miss anything, it would be the size of the zeiss... but I do not miss that lens at all as this Sony G lens has completely blown it off the water. Frankly spoken, I am amazed this lens \u201conly\u201d costs the 1300 bucks to that matter.",
        "Amazing. Selling my ziess 24-70mm because I love this so much",
    ]
