from flask import Blueprint,render_template,redirect,request,flash,url_for,session,abort
from config import ADMIN_USERNAME,ADMIN_PASSWORD

bp = Blueprint('admin', __name__)

@bp.before_request
def before_request() :
    if session.get("admin_login") is None and request.endpoint != "admin.login" :
        abort(403)

@bp.route("/admin", methods=['GET', 'POST'])
def login() :
    if request.method == "GET" :
        return render_template("admin/admin_login.html")
    
    username = request.form['username']
    password = request.form['password']

    if username != ADMIN_USERNAME or password != ADMIN_PASSWORD :
        flash("رمز عبور یا نام کاربری اشتباه است")
        return redirect(url_for("admin.login"))

    session["admin_login"] = username
    flash("با موفقیت وارد شدید")
    return redirect(url_for("admin.dashboard"))


@bp.route("/admin/logout")
def logout():
    session.pop("admin_login")  # حذف لاگین ادمین
    flash("با موفقیت از پنل مدیریت خارج شدید", "success")
    return redirect(url_for("admin.login"))


@bp.route("/admin/dashboard", methods=['GET', 'POST'])
def dashboard() :
    return render_template("admin/admin_dashboard.html")


@bp.route("/admin/dashboard/products", methods=['GET', 'POST'])
def products() :
    return render_template("admin/admin_products.html")