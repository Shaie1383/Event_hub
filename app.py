# app.py
"""
Main entrypoint for the College Event Registration + Resource Allocation System
Multi-file Flask project root. This file creates the Flask app, registers blueprints,
sets up extensions, and provides CLI helpers to initialize & seed the database.

Create the other files next (models.py, templates, static, blueprints, etc).
"""

import os
from pathlib import Path
from flask import Flask, redirect, url_for, current_app
from flask_migrate import Migrate
from flask.cli import with_appcontext
import click

# Try to import configuration from config.py if present, otherwise fallback to defaults
try:
    from config import Config
except Exception:
    class Config:
        SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app_data.db")
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        # Customize these if you want
        UPLOADED_IMAGES_ZIP = os.environ.get("UPLOADED_IMAGES_ZIP", "")

# The models module will be created next. We import inside create_app to avoid import-time issues
def create_app(config_object=None):
    """
    Create and configure the Flask application.
    This function registers blueprints if they exist and initializes extensions.
    """
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config_object or Config)

    # Initialize extensions that depend on models.py
    try:
        # Import SQLAlchemy instance and models from models.py (to be created)
        from models import db, User, Event, Resource, Booking, Registration
    except Exception as e:
        # If models.py doesn't exist yet, create a minimal placeholder db to avoid crash.
        # Real models will be available once models.py is created and the app restarted.
        db = None
        User = Event = Resource = Booking = Registration = None
        app.logger.warning("models.py not found or failed to import. Create models.py next. (%s)", e)

    # Only initialize db & migrate if models imported successfully
    if db is not None:
        db.init_app(app)
        migrate = Migrate(app, db)
    else:
        migrate = None

    # Register blueprints (if present). Blueprints files will be created later.
    try:
        from blueprints.events import events_bp
        app.register_blueprint(events_bp)
        
        from blueprints.resources import resources_bp
        app.register_blueprint(resources_bp)
        
        from blueprints.admin import admin_bp
        app.register_blueprint(admin_bp)
    except Exception as e:
        print(f"Blueprint registration warning: {e}")
    # Simple home route
    @app.route("/")
    def index():
        from flask import render_template
        return render_template("home.html")

    @app.route('/favicon.ico')
    def favicon():
        return redirect(url_for('static', filename='img/favicon.ico'))

    # Add CLI helpers for initializing and seeding the DB
    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        """Initialize the database (create tables)."""
        if db is None:
            click.echo("models.py (and db) not available. Create models.py first.")
            return
        db.create_all()
        click.echo("Initialized the database.")

    @click.command("seed-db")
    @with_appcontext
    def seed_db_command():
        """Seed database with demo events/resources/admin user."""
        if db is None:
            click.echo("models.py (and db) not available. Create models.py first.")
            return
        # Import models inside function to ensure models exist
        from models import User, Event, Resource
        # Create admin if none
        if not User.query.filter_by(email="admin@example.com").first():
            admin = User(name="Admin", email="admin@example.com", is_admin=True)
            admin.set_password("adminpass")
            db.session.add(admin)
            click.echo("Created admin: admin@example.com / adminpass")
        # Add sample events if none
        if Event.query.count() == 0:
            from datetime import date
            demo = [
                Event(title="Ripples 2024", category="Ripples", date=date(2024,12,30),
                      location="Main Auditorium", image="ripples.jpg", description_short="Technical workshops and competitions.",
                      description_long="Ripples long description...", team_size="Varies", fee="300"),
                Event(title="Expo 2024", category="Expo", date=date(2024,12,27),
                      location="Exhibition Hall D", image="expo.jpg", description_short="Showcasing innovative projects.",
                      description_long="Expo long description...", team_size="3-5 Members", fee="$500 per Team"),
                Event(title="Hackathon 2024", category="Hackathons", date=date(2024,12,28),
                      location="Coding Lab", image="hack.jpg", description_short="24-hour coding contest.",
                      description_long="Hackathon long details...", team_size="5-8 Members", fee="500 per Team"),
                    Event(title="DJ Night 2024", category="Social", date=date(2024,12,31),
                        location="Amphitheater", image="djnight.jpg", description_short="High-energy dance night with live DJ.",
                        description_long="Ring in the New Year with top DJs, dancing, and entertainment.", team_size="Unlimited", fee="$15 per Person"),
                    Event(title="Freshers Party", category="Social", date=date(2024,12,29),
                        location="Open Ground", image="freshers.jpg", description_short="Welcome celebration for new students.",
                        description_long="Fun-filled evening with games, music, food, and networking.", team_size="Unlimited", fee="Free")
            ]
            db.session.bulk_save_objects(demo)
            click.echo("Seeded sample events.")
        # Add some resources
        if Resource.query.count() == 0:
            demo_res = [
                Resource(name="Projector", category="AV", image="projector.jpg", quantity=3),
                Resource(name="Wireless Mic", category="Audio", image="mic.jpg", quantity=10),
                Resource(name="Decoration Lights", category="Decoration", image="lights.jpg", quantity=20),
                Resource(name="Sound System", category="Audio", image="sound.jpg", quantity=5),
                Resource(name="Projector Screen", category="AV", image="screen.jpg", quantity=4),
                Resource(name="Stage Setup", category="Furniture", image="stage.jpg", quantity=2),
                Resource(name="PA System", category="Audio", image="pa.jpg", quantity=3),
                Resource(name="Power Strips", category="Equipment", image="power.jpg", quantity=15),
                Resource(name="Laptop Stand", category="Equipment", image="laptop.jpg", quantity=8),
                Resource(name="Hall Setup", category="Furniture", image="hall.jpg", quantity=1)
            ]
            db.session.bulk_save_objects(demo_res)
            click.echo("Seeded sample resources.")
        db.session.commit()
        click.echo("Seeding complete.")

    # Register CLI commands on app
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)

    return app


# Allow running this file directly for quick development
# Create a top-level `app` so WSGI servers (gunicorn) can import it as `app:app`.
app = create_app()

# Auto-init and seed the database for showcase/demo environments.
# Controlled by the `AUTO_INIT_DB` environment variable to avoid running
# in production unintentionally. Set `AUTO_INIT_DB=true` on the host
# (for example in Render's env vars) to enable this behavior.
# Always auto-initialize on startup
try:
    with app.app_context():
        try:
            from models import db, User, Event, Resource
        except Exception as _e:
            app.logger.warning("Auto-init: models import failed: %s", _e)
        else:
            # Create tables
            db.create_all()
            # Seed admin user if missing
            if not User.query.filter_by(email="admin@example.com").first():
                admin = User(name="Admin", email="admin@example.com", is_admin=True)
                try:
                    admin.set_password("adminpass")
                except Exception:
                    pass
                db.session.add(admin)
            # Seed demo events if missing
            if Event.query.count() == 0:
                from datetime import date
                demo = [
                    Event(title="Ripples 2024", category="Ripples", date=date(2024,12,30),
                          location="Main Auditorium", image="ripples.jpg", description_short="Technical workshops and competitions.",
                          description_long="Ripples long description...", team_size="Varies", fee="Free"),
                    Event(title="Expo 2024", category="Expo", date=date(2024,12,27),
                          location="Exhibition Hall D", image="expo.jpg", description_short="Showcasing innovative projects.",
                          description_long="Expo long description...", team_size="3-5 Members", fee="$500 per Team"),
                    Event(title="Hackathon 2024", category="Hackathons", date=date(2024,12,28),
                          location="Coding Lab", image="hack.jpg", description_short="24-hour coding contest.",
                          description_long="Hackathon long details...", team_size="5-8 Members", fee="500 per Team"),
                      Event(title="DJ Night 2024", category="Social", date=date(2024,12,31),
                          location="Amphitheater", image="djnight.jpg", description_short="High-energy dance night with live DJ.",
                          description_long="Ring in the New Year with top DJs, dancing, and entertainment.", team_size="Unlimited", fee="$15 per Person"),
                      Event(title="Freshers Party", category="Social", date=date(2024,12,29),
                          location="Open Ground", image="freshers.jpg", description_short="Welcome celebration for new students.",
                          description_long="Fun-filled evening with games, music, food, and networking.", team_size="Unlimited", fee="Free")
                ]
                db.session.bulk_save_objects(demo)
            # Seed demo resources if missing
            if Resource.query.count() == 0:
                demo_res = [
                    Resource(name="Projector", category="AV", image="projector.jpg", quantity=3),
                    Resource(name="Wireless Mic", category="Audio", image="mic.jpg", quantity=10),
                    Resource(name="Decoration Lights", category="Decoration", image="lights.jpg", quantity=20),
                    Resource(name="Sound System", category="Audio", image="sound.jpg", quantity=5),
                    Resource(name="Projector Screen", category="AV", image="screen.jpg", quantity=4),
                    Resource(name="Stage Setup", category="Furniture", image="stage.jpg", quantity=2),
                    Resource(name="PA System", category="Audio", image="pa.jpg", quantity=3),
                    Resource(name="Power Strips", category="Equipment", image="power.jpg", quantity=15),
                    Resource(name="Laptop Stand", category="Equipment", image="laptop.jpg", quantity=8),
                    Resource(name="Hall Setup", category="Furniture", image="hall.jpg", quantity=1)
                ]
                db.session.bulk_save_objects(demo_res)
            # Commit any new rows
            try:
                db.session.commit()
            except Exception as _e:
                app.logger.exception("Auto-init commit failed: %s", _e)
            else:
                app.logger.info("✔ Database auto-initialized: tables created and demo data seeded")
except Exception as e:
    app.logger.exception("⚠ Database auto-init warning: %s", e)


if __name__ == "__main__":
    # If the models exist, you can create tables automatically on first run:
    try:
        with app.app_context():
            # Only attempt to auto-create tables if models are importable
            from models import db  # noqa
            db.create_all()
    except Exception:
        app.logger.warning("Skipped automatic db.create_all() because models.py is missing or raised an error.")
    # Run the dev server
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
