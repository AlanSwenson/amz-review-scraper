from functools import wraps

from flask import flash, redirect, url_for
import amz_review_scraper.models.user as user_methods


def check_confirmed(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        current_user = user_methods.get_current_user()
        if current_user.confirmed is False:
            flash("Please confirm your account!", "warning")
            return redirect(url_for("signup.unconfirmed"))
        return func(*args, **kwargs)

    return decorated_function
