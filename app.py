# app.py
"""
Main entrypoint for the College Event Registration + Resource Allocation System
Multi-file Flask project root. This file creates the Flask app, registers blueprints,
sets up extensions, and provides CLI helpers to initialize & seed the database.
"""

import os
from flask import Flask
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click

# Try to import configuration from config.py if present, otherwise fallback to defaults
try:
    from config import Config
except Exception:
    class Config:
        SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
        SQLALCHEMY_DATABASE_URI = os.environ.get(
            "DATABASE_URL", "sqlite:///app_data.db"
        )
        SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app(config_object=None):
    """
    Main Flask application factory.
    """
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_object or Config)

    # Try importing models
    try:
        from models import db, User, Event, Resource, Booking, Registration
    except Exception as e:
        db = None
        User = Event = Resource = Booking = Registration = None
        app.logger.warning(f"models.py not found or broken: {e}")

    # Initialize DB + Migrations
    if db is not None:
        db.init_app(app)
        migrate = Migrate(app, db)
    else:
        migrate = None

    # Register blueprints
    try:
        from blueprints.events import events_bp
        from blueprints.resources import resources_bp
        from blueprints.admin import admin_bp

        app.register_blueprint(events_bp)
        app.register_blueprint(resources_bp)
        app.register_blueprint(admin_bp)

    except Exception as e:
        print(f"Blueprint registration warning: {e}")

    # Home route
    @app.route("/")
    def index():
        from flask import render_template
        return render_template("home.html")

    # CLI Commands -------------------------------------------------------------
    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        """Initialize database."""
        if db is None:
            click.echo("models.py missing.")
            return
        db.create_all()
        click.echo("Database initialized.")

    @click.command("seed-db")
    @with_appcontext
    def seed_db_command():
        """Seed sample data."""
        if db is None:
            click.echo("models.py missing.")
            return

        from models import User, Event, Resource
        from datetime import date

        # Admin
        if not User.query.filter_by(email="admin@example.com").first():
            admin = User(name="Admin", email="admin@example.com", is_admin=True)
            admin.set_password("adminpass")
            db.session.add(admin)

        # Events
        if Event.query.count() == 0:
            demo = [
                Event(
                    title="Ripples 2024",
                    category="Ripples",
                    date=date(2024, 12, 30),
                    location="Main Auditorium",
                    image="ripples.jpg",
                    description_short="Technical workshops and competitions.",
                    description_long="Ripples long description...",
                    team_size="Varies",
                    fee="Free",
                ),
                Event(
                    title="Expo 2024",
                    category="Expo",
                    date=date(2024, 12, 27),
                    location="Exhibition Hall D",
                    image="expo.jpg",
                    description_short="Showcasing innovative projects.",
                    description_long="Expo long description...",
                    team_size="3-5 Members",
                    fee="$500 per Team",
                ),
                Event(
                    title="Hackathon 2024",
                    category="Hackathons",
                    date=date(2024, 12, 28),
                    location="Coding Lab",
                    image="hack.jpg",
                    description_short="24-hour coding contest.",
                    description_long="Hackathon long details...",
                    team_size="5-8 Members",
                    fee="500 per Team",
                ),
            ]
            db.session.bulk_save_objects(demo)

        # Resources
        if Resource.query.count() == 0:
            demo_res = [
                Resource(
                    name="Projector",
                    category="AV",
                    image="projector.jpg",
                    quantity=3,
                ),
                Resource(
                    name="Wireless Mic",
                    category="Audio",
                    image="mic.jpg",
                    quantity=10,
                ),
                Resource(
                    name="Decoration Lights",
                    category="Decoration",
                    image="lights.jpg",
                    quantity=20,
                ),
            ]
            db.session.bulk_save_objects(demo_res)

        db.session.commit()
        click.echo("Seeding complete.")

    # Register CLI Commands
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)

    # -------------------------------------------------------------------------
    # AUTO INITIALIZE & SEED DATABASE ON RENDER
    # -------------------------------------------------------------------------
    if db is not None:
        with app.app_context():
            try:
                from models import db, Event, Resource, User
                from datetime import date

                db.create_all()  # Creates table if missing

                # -------- Seed Events --------
                if Event.query.count() == 0:
                    demo = [
                        Event(
                            title="Ripples 2024",
                            category="Ripples",
                            date=date(2024, 12, 30),
                            location="Main Auditorium",
                            image="ripples.jpg",
                            description_short="Technical workshops and competitions.",
                            description_long="Ripples long description...",
                            team_size="Varies",
                            fee="Free",
                        ),
                        Event(
                            title="Expo 2024",
                            category="Expo",
                            date=date(2024, 12, 27),
                            location="Exhibition Hall D",
                            image="expo.jpg",
                            description_short="Showcasing innovative projects.",
                            description_long="Expo long description...",
                            team_size="3-5 Members",
                            fee="$500 per Team",
                        ),
                        Event(
                            title="Hackathon 2024",
                            category="Hackathons",
                            date=date(2024, 12, 28),
                            location="Coding Lab",
                            image="hack.jpg",
                            description_short="24-hour coding contest.",
                            description_long="Hackathon long details...",
                            team_size="5-8 Members",
                            fee="500 per Team",
                        ),
                    ]
                    db.session.bulk_save_objects(demo)

                # -------- Seed Resources --------
                if Resource.query.count() == 0:
                    demo_res = [
                        Resource(
                            name="Projector",
                            category="AV",
                            image="projector.jpg",
                            quantity=3,
                        ),
                        Resource(
                            name="Wireless Mic",
                            category="Audio",
                            image="mic.jpg",
                            quantity=10,
                        ),
                        Resource(
                            name="Decoration Lights",
                            category="Decoration",
                            image="lights.jpg",
                            quantity=20,
                        ),
                    ]
                    db.session.bulk_save_objects(demo_res)

                # -------- Seed Admin --------
                if not User.query.filter_by(email="admin@example.com").first():
                    admin = User(
                        name="Admin",
                        email="admin@example.com",
                        is_admin=True,
                    )
                    admin.set_password("adminpass")
                    db.session.add(admin)

                db.session.commit()
                print("✔ Auto database setup completed")

            except Exception as e:
                print("⚠ Auto DB setup error:", e)

    return app


# ------------------------------------------------------------------------------
# Expose app for gunicorn
# ------------------------------------------------------------------------------
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        try:
            from models import db
            db.create_all()
        except:
            print("Local DB init skipped.")
    app.run(debug=True)
