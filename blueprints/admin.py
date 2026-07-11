from flask import Blueprint,render_template,redirect,request,flash,url_for,session,abort,current_app
from config import ADMIN_USERNAME,ADMIN_PASSWORD
from models.tables import Service
from extentions import db


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
        flash("رمز عبور یا نام کاربری اشتباه است", "error")
        return redirect(url_for("admin.login"))

    session["admin_login"] = username
    flash("با موفقیت وارد شدید", "success")
    return redirect(url_for("admin.dashboard"))


@bp.route("/admin/logout")
def logout():
    session.pop("admin_login")  # حذف لاگین ادمین
    flash("با موفقیت از پنل مدیریت خارج شدید", "success")
    return redirect(url_for("admin.login"))


@bp.route("/admin/dashboard", methods=['GET', 'POST'])
def dashboard() :
    if request.method == "GET" :
        return render_template("admin/admin_dashboard.html")
    
    title = request.form["title"].strip()
    description = request.form["description"].strip()
    icon = request.files.get("icon")
    
    active = "active" in request.form


    service = Service(
        title=title,
        description=description,
        active=active
    )


    db.session.add(service)
    db.session.commit()

    if icon and icon.filename != '':
        icon.save(f'static/cover/{ service.id }.jpg')

    return redirect(url_for("admin.dashboard"))








    