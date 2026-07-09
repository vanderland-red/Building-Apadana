from flask import Blueprint
from extentions import db

bp = Blueprint('general', __name__)

@bp.route("/")
def home ():
    return "WELCOME THE MAJESTY MAN"
