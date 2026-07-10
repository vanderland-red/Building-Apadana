from flask import Blueprint,render_template,redirect,request,url_for,flash,session
from models.tables import User
from extentions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required,current_user,logout_user
import re

bp = Blueprint('user', __name__)

@bp.route("/user/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template('user/user_login.html')
    
    fullname = request.form['fullname'].strip()
    phone = request.form['phone'].strip()
    email = request.form['email'].strip()
    password = request.form['password'].strip()
    password_2 = request.form['password_2'].strip()

    if not fullname or not phone or not password or not password_2:
        flash("لطفا فیلد های مهم را پر کنید", "warning")
        return redirect(url_for("user.register"))


    if len(fullname) < 5:
        flash("لطفا نام و نام خانوادگی را کامل وارد کنید", "warning")
        return redirect(url_for("user.register"))
    
    if len(password) < 5:
        flash("لطفا رمز عبور سخت تری را انتخاب کنید", "error")
        return redirect(url_for("user.register"))

    if password != password_2:
        flash("رمز های عبور مطابق هم نیست", "error")
        return redirect(url_for("user.register"))
    
    if not re.fullmatch(r"(?:\+98|0)9\d{9}", phone):
        flash("شماره موبایل وارد شده صحیح نیست", "warning")
        return redirect(url_for("user.register"))

    
    
    
    existing_phone = User.query.filter_by(phone=phone).first()
    if existing_phone:
        flash("این شماره موبایل قبلاً ثبت شده است", "warning")
        return redirect(url_for("user.register"))
    
    if email:
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            flash("این ایمیل قبلاً ثبت شده است", "warning")
            return redirect(url_for("user.register"))
    

    save_user = User(
        fullname= fullname,
        phone= phone,
        email= email,
        password=generate_password_hash(password)
    )
    
    db.session.add(save_user)
    db.session.commit()

    login_user(save_user)

    flash("ثبت نام با موفقیت انجام شد", "success")
    return redirect(url_for("general.home"))





@bp.route("/user/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template('user/user_login.html')