from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from flask import current_app as app
from flask import render_template, url_for

from amz_review_scraper import mail


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
    except:
        return False
    return email


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.send(msg)


def send_reset_email(user):
    token = generate_confirmation_token(user.email)
    confirm_url = url_for("user.reset_token", token=token, _external=True)
    html = render_template("email/reset_password_email.html", confirm_url=confirm_url)
    subject = "Reset Password - Peachtools.com"
    send_email(user.email, subject, html)
