from flask import redirect, render_template, url_for, Blueprint

admin_blueprint = Blueprint("admin", __name__, template_folder="templates")
