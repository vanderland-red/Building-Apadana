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
        services = Service.query.all()
        return render_template("admin/admin_dashboard.html", services=services)
    
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

    # چون هنوز شناسه سرویس آیدی ساخته نشده یاید بعد از کامییت فایل عکس ذخیره بشه
    if icon and icon.filename != '':
        icon.save(f'static/cover/{ service.id }.jpg')

    flash("سرویس با موفقیت اضافه شد", "success")
    return redirect(url_for("admin.dashboard"))



@bp.route("/admin/dashboard/delete/<int:id>")
def delete_service(id):

    service = Service.query.get_or_404(id)

    db.session.delete(service)
    db.session.commit()

    return redirect(url_for("admin.dashboard"))




@bp.route("/admin/dashboard/edit/<int:id>", methods=["GET", "POST"])
def edit_service(id):
    service = Service.query.get_or_404(id)

    if request.method == "GET" :
        return render_template("admin/admin_edit_service.html", service=service)

    title = request.form["title"]
    icon = request.files.get("icon")
    active = "active" in request.form

    service.title = title
    service.active = active

    if icon and icon.filename:
        icon.save(f'static/cover/{service.id}.jpg')

    db.session.commit()
    
    flash("سرویس با موفقیت تغییر یافت", "success")
    return redirect(url_for("admin.dashboard"))


