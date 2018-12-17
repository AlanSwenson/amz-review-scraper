from amz_review_scraper import db

users_items_association = db.Table(
    "users_items",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("item_id", db.Integer, db.ForeignKey("items.id")),
)
