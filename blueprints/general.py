from flask import Blueprint

bp = Blueprint('general', __name__)

@bp.route("/")
def home ():
    return "WELCOME THE MAJESTY MAN"
