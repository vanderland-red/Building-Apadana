from flask import Blueprint,render_template
from models.tables import Service

bp = Blueprint('general', __name__)

@bp.route("/")
def home ():

    services = Service.query.filter(Service.active == True).all()

    return render_template("home.html", services=services)


@bp.route("/about-apadana")
def about ():
    return render_template("about.html")
