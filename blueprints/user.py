from flask import Blueprint

bp = Blueprint('user', __name__)

@bp.route("/user")
def user() :
    return "WELCOME THE User Page"
