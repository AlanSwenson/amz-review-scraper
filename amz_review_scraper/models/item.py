from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timezone

from amz_review_scraper import db
from amz_review_scraper.models.users_items_association import users_items_association


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(10), unique=True)
    name = db.Column(db.String)
    customer_reviews_count = db.Column(db.Integer)
    reviews = db.relationship("Review", backref="owner", lazy=True)
    last_scraped = db.Column(
        db.DateTime(timezone=True), nullable=False, default=datetime.utcnow()
    )
    users = db.relationship("User", secondary=users_items_association, backref="item")

    def add(self, user):
        scraped_item = self
        existing_item = get_results(asin=self.asin)
        if existing_item is None:
            user.items.append(scraped_item)
        else:
            item_link = is_item_linked_to_user(scraped_item, user)
            if item_link is None:
                user.items.append(existing_item)
            scraped_item = save_or_update(scraped_item)
        return scraped_item


def get_results(asin=None, user_id=None):
    if asin is not None:
        return Item.query.filter_by(asin=asin).one_or_none()
    elif user_id is not None:
        return Item.query.join(
            users_items_association, (users_items_association.c.user_id == user_id)
        ).filter(users_items_association.c.item_id == Item.id)
    else:
        return Item.query.all()


def is_item_linked_to_user(self, user):
    return (
        Item.query.join(
            users_items_association, (users_items_association.c.user_id == user.id)
        )
        .filter(users_items_association.c.item_id == Item.id)
        .filter(Item.asin == self.asin)
        .first()
    )


def save_or_update(self):
    self.last_scraped = datetime.utcnow()
    stmt = insert(Item).values(
        asin=self.asin,
        name=self.name,
        customer_reviews_count=self.customer_reviews_count,
        last_scraped=self.last_scraped,
    )
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=["asin"],
        set_={
            "customer_reviews_count": self.customer_reviews_count,
            "last_scraped": self.last_scraped,
        },
    )
    db.session.execute(do_update_stmt)
    return get_results(asin=self.asin)
