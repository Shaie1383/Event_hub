# blueprints/events.py

from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
from models import db, Event, Registration

events_bp = Blueprint("events_bp", __name__, template_folder="../templates")


# -------------------------
# EVENTS LIST PAGE
# -------------------------
@events_bp.route("/events")
def list_events():
    q = request.args.get("q", "")
    category = request.args.get("category", "")
    sort = request.args.get("sort", "date")

    evs = Event.query

    if q:
        evs = evs.filter(Event.title.ilike(f"%{q}%"))

    if category:
        evs = evs.filter(Event.category == category)

    # Sorting
    if sort == "date":
        evs = evs.order_by(Event.date.asc())
    elif sort == "title_asc":
        evs = evs.order_by(Event.title.asc())
    elif sort == "title_desc":
        evs = evs.order_by(Event.title.desc())

    events_list = evs.all()

    return render_template("events.html", events=events_list, q=q, category=category, sort=sort)


# -------------------------
# EVENT DETAIL
# -------------------------
@events_bp.route("/event/<int:event_id>")
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)

    # SPECIAL FEATURE:
    # If the event is "Ripples", show technical + non-technical
    technical_events = []
    non_technical_events = []

    if event.category.lower() == "ripples":
        technical_events = [
            {"title": "Coding", "fee": "100", "team_size": "1 member",
             "desc": "Test your problem-solving skills in coding."},

            {"title": "Poster Presentation", "fee": "50", "team_size": "1-2 members",
             "desc": "Present creative posters on innovation."},

            {"title": "Paper Presentation", "fee": "50", "team_size": "1-2 members",
             "desc": "Showcase your research paper."},

            {"title": "Quiz", "fee": "100", "team_size": "2 members",
             "desc": "Tech-based quiz contest."}
        ]

        non_technical_events = [
            {"title": "Stalls", "fee": "300", "team_size": "4-6 members",
             "desc": "Game & food stalls."},

            {"title": "Treasure Hunt", "fee": "100", "team_size": "2-3 members",
             "desc": "Fun treasure hunt event."},

            {"title": "Dance", "fee": "150", "team_size": "Solo or Team",
             "desc": "Dance performance event."},

            {"title": "Flash Mob", "fee": "Free", "team_size": "Team",
             "desc": "Energetic group performance."}
        ]

    return render_template(
        "event_detail.html",
        event=event,
        technical_events=technical_events,
        non_technical_events=non_technical_events
    )


# -------------------------
# EVENT DETAILS API (for AJAX modal)
# -------------------------
@events_bp.route("/api/event/<int:event_id>")
def api_event(event_id):
    event = Event.query.get_or_404(event_id)

    return jsonify({
        "id": event.id,
        "title": event.title,
        "category": event.category,
        "date": event.date.isoformat() if event.date else None,
        "location": event.location,
        "image": event.image,
        "description_short": event.description_short,
        "description_long": event.description_long,
        "team_size": event.team_size,
        "fee": event.fee
    })


# -------------------------
# EVENT REGISTRATION (Modal popup form)
# -------------------------
@events_bp.route("/register-event", methods=["POST"])
def register_event():
    data = request.form

    event_id = data.get("event_id")
    name = data.get("name")
    regno = data.get("regno")
    email = data.get("email")
    mobile = data.get("mobile")
    year = data.get("year")

    if not (event_id and name and regno and email):
        return jsonify({"error": "Missing required fields"}), 400

    reg = Registration(
        event_id=event_id,
        name=name,
        regno=regno,
        email=email,
        mobile=mobile,
        year=year
    )

    db.session.add(reg)
    db.session.commit()

    return jsonify({"message": "Registration successful!"})
