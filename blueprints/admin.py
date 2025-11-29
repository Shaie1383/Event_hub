# blueprints/admin.py

from flask import (
    Blueprint, render_template, request, redirect,
    url_for, flash, session
)
from models import db, User, Event, Resource, Booking, Registration
from werkzeug.security import check_password_hash

admin_bp = Blueprint("admin_bp", __name__, template_folder="../templates")


# ---------------------------------------------------------
#  ADMIN AUTH MIDDLEWARE
# ---------------------------------------------------------
def admin_required():
    if not session.get("is_admin"):
        flash("Please login as admin", "danger")
        return False
    return True


# ---------------------------------------------------------
#  LOGIN PAGE
# ---------------------------------------------------------
@admin_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # Showcase mode - accept any email/password combination
        if not email or not password:
            flash("Email and password required", "danger")
            return redirect(url_for("admin_bp.admin_login"))

        session["is_admin"] = True
        session["admin_name"] = email.split("@")[0] if "@" in email else email

        flash("Logged in successfully", "success")
        return redirect(url_for("admin_bp.admin_dashboard"))

    return render_template("admin_login.html")


# ---------------------------------------------------------
#  LOGOUT
# ---------------------------------------------------------
@admin_bp.route("/admin/logout")
def admin_logout():
    session.clear()
    flash("Logged out", "info")
    return redirect(url_for("events_bp.events_page"))


# ---------------------------------------------------------
#  ADMIN DASHBOARD
# ---------------------------------------------------------
@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    if not admin_required():
        return redirect(url_for("admin_bp.admin_login"))

    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    registrations = Registration.query.order_by(Registration.created_at.desc()).all()
    resources = Resource.query.order_by(Resource.name.asc()).all()
    events = Event.query.order_by(Event.date.asc()).all()

    return render_template(
        "admin_dashboard.html",
        bookings=bookings,
        registrations=registrations,
        resources=resources,
        events=events,
        admin=session.get("admin_name")
    )


# ---------------------------------------------------------
#  APPROVE BOOKING
# ---------------------------------------------------------
@admin_bp.route("/admin/booking/<int:bid>/approve")
def admin_approve(bid):
    if not admin_required():
        return redirect(url_for("admin_bp.admin_login"))

    booking = Booking.query.get_or_404(bid)
    booking.status = "Approved"
    db.session.commit()

    flash("Booking Approved", "success")
    return redirect(url_for("admin_bp.admin_dashboard"))


# ---------------------------------------------------------
#  REJECT BOOKING
# ---------------------------------------------------------
@admin_bp.route("/admin/booking/<int:bid>/reject")
def admin_reject(bid):
    if not admin_required():
        return redirect(url_for("admin_bp.admin_login"))

    booking = Booking.query.get_or_404(bid)
    booking.status = "Rejected"
    db.session.commit()

    flash("Booking Rejected", "info")
    return redirect(url_for("admin_bp.admin_dashboard"))


# ---------------------------------------------------------
#  ADD RESOURCE (You requested “add resources all at once”)
# ---------------------------------------------------------
@admin_bp.route("/admin/resource/add", methods=["POST"])
def admin_add_resource():
    if not admin_required():
        return redirect(url_for("admin_bp.admin_login"))

    name = request.form.get("name")
    category = request.form.get("category")
    quantity = request.form.get("quantity")
    image = request.form.get("image")  # filename only

    if not name:
        flash("Resource name required", "danger")
        return redirect(url_for("admin_bp.admin_dashboard"))

    res = Resource(
        name=name,
        category=category,
        image=image or "placeholder.jpg",
        quantity=int(quantity or 1)
    )

    db.session.add(res)
    db.session.commit()

    flash(f"Resource '{name}' added", "success")
    return redirect(url_for("admin_bp.admin_dashboard"))


# ---------------------------------------------------------
#  DELETE RESOURCE
# ---------------------------------------------------------
@admin_bp.route("/admin/resource/<int:rid>/delete")
def admin_delete_resource(rid):
    if not admin_required():
        return redirect(url_for("admin_bp.admin_login"))

    res = Resource.query.get_or_404(rid)
    db.session.delete(res)
    db.session.commit()

    flash("Resource deleted", "info")
    return redirect(url_for("admin_bp.admin_dashboard"))


# ---------------------------------------------------------
#  UPDATE RESOURCE
# ---------------------------------------------------------
@admin_bp.route("/admin/resource/<int:rid>/update", methods=["POST"])
def admin_update_resource(rid):
    if not admin_required():
        return redirect(url_for("admin_bp.admin_login"))

    res = Resource.query.get_or_404(rid)

    res.name = request.form.get("name") or res.name
    res.category = request.form.get("category") or res.category
    res.quantity = int(request.form.get("quantity") or res.quantity)
    res.image = request.form.get("image") or res.image

    db.session.commit()

    flash("Resource updated", "success")
    return redirect(url_for("admin_bp.admin_dashboard"))
