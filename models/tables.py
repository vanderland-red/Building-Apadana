from extentions import SQLAlchemy
from datetime import datetime
from extentions import db
from flask_login import UserMixin




class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")# نقش کاربر
    created_at = db.Column(db.DateTime, default=datetime.utcnow)# زمان ثبت نام

    def __repr__(self):
        return f"<User {self.fullname}>"
    



class Service(db.Model):
    __tablename__ = "service"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True, nullable=False)





class ServiceRequest(db.Model):
    __tablename__ = "service_request"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    service_id = db.Column(
        db.Integer,
        db.ForeignKey("service.id"),
        nullable=False
    )


    address = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="user_service_requests")
    service = db.relationship("Service", backref="service_requests")
    request_images = db.relationship(
        "RequestImage",
        back_populates="service_request",
        cascade="all, delete-orphan"
    )

    def status_farsi(self) :
        if self.status == "reject" :
            return "رد شده"
        
        if self.status == "accept" :
            return "قبول"



class RequestImage(db.Model):
    __tablename__ = "request_image"

    id = db.Column(db.Integer, primary_key=True)

    request_id = db.Column(
        db.Integer,
        db.ForeignKey("service_request.id"),
        nullable=False
    )

    image_path = db.Column(db.String(255), nullable=False)

    service_request = db.relationship("ServiceRequest",back_populates="request_images")

