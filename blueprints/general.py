from flask import Blueprint,render_template
from models.tables import Service

bp = Blueprint("general", __name__, url_prefix="/general") # باعث میشه دیگه نخواد قبل آدرس های روت نام جنرال را نوشت

@bp.route("/")
def home ():

    services = Service.query.filter(Service.active == True).all()

    return render_template("home.html", services=services)


@bp.route("/about-apadana")
def about ():
    return render_template("about.html")

@bp.route("/projeha-apadana")
def projeha ():
    return render_template("user/another_page/projeha.html")

@bp.route("/roidad-ha-apadana")
def roidad_ha ():
    return render_template("user/another_page/roidad_ha.html")

@bp.route("/tamas-ba-ma-apadana")
def tamas_ba_ma ():
    return render_template("user/another_page/tamas_ba_ma.html")

