# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# ---------------------------------------------------
# USER MODEL
# ---------------------------------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    email = db.Column(db.String(140), unique=True, index=True)
    password_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)

    registrations = db.relationship("Registration", backref="user", lazy=True)
    bookings = db.relationship("Booking", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if self.password_hash:
            return check_password_hash(self.password_hash, password)
        return False


# ---------------------------------------------------
# EVENT MODEL
# ---------------------------------------------------
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)  
    date = db.Column(db.Date)
    location = db.Column(db.String(255))
    image = db.Column(db.String(255))  
    description_short = db.Column(db.Text)
    description_long = db.Column(db.Text)
    team_size = db.Column(db.String(100))
    fee = db.Column(db.String(100))

    registrations = db.relationship("Registration", backref="event", lazy=True)


# ---------------------------------------------------
# REGISTRATION MODEL
# ---------------------------------------------------
class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    name = db.Column(db.String(200))
    regno = db.Column(db.String(100))
    email = db.Column(db.String(120))
    mobile = db.Column(db.String(50))
    year = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------------------------------------------
# RESOURCE MODEL
# ---------------------------------------------------
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))  # Audio, AV, Decoration, Hall, etc.
    image = db.Column(db.String(255))
    quantity = db.Column(db.Integer, default=1)

    bookings = db.relationship("Booking", backref="resource", lazy=True)


# ---------------------------------------------------
# BOOKING MODEL
# ---------------------------------------------------
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey("resource.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    event_name = db.Column(db.String(200))  # e.g., Ripples Coding Contest
    purpose = db.Column(db.Text)

    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    status = db.Column(db.String(30), default="Pending")  
    # Pending / Approved / Rejected

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
