# blueprints/resources.py

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from datetime import datetime
from sqlalchemy import and_, or_
from models import db, Resource, Booking

resources_bp = Blueprint("resources_bp", __name__, template_folder="../templates")


# ---------------------------------------------------------
# RESOURCE LIST PAGE (with search + filters)
# ---------------------------------------------------------
@resources_bp.route("/resources")
def resources_page():
    q = request.args.get("q", "")
    category = request.args.get("category", "")
    sort = request.args.get("sort", "az")

    res = Resource.query

    # search
    if q:
        res = res.filter(Resource.name.ilike(f"%{q}%"))

    # category filter
    if category:
        res = res.filter(Resource.category == category)

    # sorting options
    if sort == "az":
        res = res.order_by(Resource.name.asc())
    elif sort == "za":
        res = res.order_by(Resource.name.desc())

    resources = res.all()

    # Suggestions for ripple events
    # (Displayed in UI as icons/cards)
    suggestions = [
        {"name": "Projector", "reason": "Useful for coding & paper presentation"},
        {"name": "Wireless Mic", "reason": "For announcements & hosting"},
        {"name": "Decoration Lights", "reason": "For stalls & stage"},
        {"name": "Gallery Hall", "reason": "For large gatherings"},
    ]

    return render_template(
        "resources.html",
        resources=resources,
        q=q,
        category=category,
        sort=sort,
        suggestions=suggestions
    )


# ---------------------------------------------------------
# API FOR AJAX SUGGESTIONS
# ---------------------------------------------------------
@resources_bp.route("/api/resources/suggestions")
def resource_suggestions():
    data = [
        "Projector", "Wireless Mic", "PA System",
        "Decoration Lights", "Laptop", "Gallery Hall"
    ]
    return jsonify({"suggestions": data})


# ---------------------------------------------------------
# API FOR CART SUPPORT (optional)
# ---------------------------------------------------------
@resources_bp.route("/api/resource/<int:rid>")
def api_get_resource(rid):
    r = Resource.query.get_or_404(rid)
    return jsonify({
        "id": r.id,
        "name": r.name,
        "category": r.category,
        "image": r.image,
        "quantity": r.quantity
    })


# ---------------------------------------------------------
# BOOK A RESOURCE (form submission)
# ---------------------------------------------------------
@resources_bp.route("/book-resource", methods=["POST"])
def book_resource():
    form = request.form if request.form else request.json

    try:
        resource_id = int(form.get("resource_id"))
    except:
        flash("Invalid resource selected", "danger")
        return redirect(url_for("resources_bp.resources_page"))

    name = form.get("name")
    regno = form.get("regno")
    email = form.get("email")
    mobile = form.get("mobile")
    branch = form.get("branch")
    year = form.get("year")
    event_name = form.get("event_name")
    purpose = form.get("purpose")

    start_date = form.get("start_date")
    end_date = form.get("end_date")

    # Date validation
    if not start_date or not end_date:
        flash("Please select valid dates", "danger")
        return redirect(url_for("resources_bp.resources_page"))

    sd = datetime.fromisoformat(start_date).date()
    ed = datetime.fromisoformat(end_date).date()

    if sd > ed:
        flash("Start date cannot be after End date", "danger")
        return redirect(url_for("resources_bp.resources_page"))

    # ---------------------------------------------------------
    # CONFLICT DETECTION (Approved bookings only)
    # ---------------------------------------------------------
    conflict = Booking.query.filter(
        Booking.resource_id == resource_id,
        Booking.status == "Approved",
        or_(
            and_(Booking.start_date <= sd, Booking.end_date >= sd),
            and_(Booking.start_date <= ed, Booking.end_date >= ed),
            and_(Booking.start_date >= sd, Booking.end_date <= ed),
        )
    ).first()

    if conflict:
        flash("Resource is already booked for selected dates.", "danger")
        return redirect(url_for("resources_bp.resources_page"))

    # ---------------------------------------------------------
    # CREATE BOOKING
    # ---------------------------------------------------------
    booking = Booking(
        resource_id=resource_id,
        event_name=event_name,
        purpose=purpose,
        start_date=sd,
        end_date=ed,
        status="Pending"  # Admin will approve
    )

    db.session.add(booking)
    db.session.commit()

    flash("Your booking request is submitted. Admin will approve soon.", "success")
    return redirect(url_for("resources_bp.resources_page"))
