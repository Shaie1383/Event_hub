#!/usr/bin/env python3
"""
Seed database with sample events and resources
Run with: python seed_data.py
"""

from app import create_app
from models import db, Event, Resource, User
from datetime import datetime, timedelta

def seed_database():
    """Add sample events, resources, and admin user"""
    
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional)
        # db.drop_all()
        # db.create_all()
        
        # Create admin user if doesn't exist
        admin = User.query.filter_by(email="admin@college.com").first()
        if not admin:
            admin = User(name="Admin", email="admin@college.com", is_admin=True)
            admin.set_password("admin123")
            db.session.add(admin)
            db.session.commit()
            print("✓ Admin user created (email: admin@college.com, password: admin123)")
        else:
            print("✓ Admin user already exists")
        
        # Check if data already exists
        if Event.query.first() is not None:
            print("✓ Database already has events. Skipping event/resource seed.")
            return
        
        # SAMPLE EVENTS
        events = [
            Event(
                title="Ripples 2024",
                category="Non-Technical",
                date=datetime.now() + timedelta(days=15),
                location="Main Auditorium",
                image="ripples.jpg",
                description_short="Inter-college cultural and talent show",
                description_long="Ripples 2024 is our annual inter-college cultural event featuring music, dance, drama, and talent competitions. Teams compete for exciting prizes and recognition. Open for all students.",
                team_size=6,
                fee=0
            ),
            Event(
                title="Code Hackathon 2024",
                category="Hackathons",
                date=datetime.now() + timedelta(days=20),
                location="Computer Lab Building",
                image="hackathon.jpg",
                description_short="24-hour coding competition",
                description_long="Code Hackathon is a 24-hour programming competition where teams solve real-world problems using code. Mentors, prizes, and industry networking opportunities available.",
                team_size=4,
                fee=500
            ),
            Event(
                title="Tech Expo 2024",
                category="Workshops",
                date=datetime.now() + timedelta(days=25),
                location="Convention Center",
                image="expo.jpg",
                description_short="Technology exhibition and workshops",
                description_long="Tech Expo showcases the latest in technology, AI, ML, and emerging tech. Includes hands-on workshops from industry experts and interactive stalls.",
                team_size=3,
                fee=200
            ),
            Event(
                title="Freshers Party 2024",
                category="Non-Technical",
                date=datetime.now() + timedelta(days=10),
                location="Amphitheater",
                image="freshers.jpg",
                description_short="Welcome event for first-year students",
                description_long="Freshers Party is a grand welcome event for new students featuring performances, games, prizes, and networking opportunities with seniors.",
                team_size=5,
                fee=100
            ),
            Event(
                title="DJ Night",
                category="Non-Technical",
                date=datetime.now() + timedelta(days=12),
                location="Open Ground",
                image="djnight.jpg",
                description_short="Evening of music and dance",
                description_long="DJ Night brings popular DJs to perform the latest hits. Dance floor, light shows, and food stalls available. Open to all students.",
                team_size=0,
                fee=150
            ),
        ]
        
        # SAMPLE RESOURCES
        resources = [
            Resource(name="Wireless Microphone System", category="Audio", image="mic.jpg", quantity=5),
            Resource(name="Projector HD", category="AV", image="projector.jpg", quantity=3),
            Resource(name="Projection Screen", category="AV", image="screen.jpg", quantity=2),
            Resource(name="LED Lights Kit", category="Decoration", image="lights.jpg", quantity=8),
            Resource(name="Main Hall", category="Hall", image="hall.jpg", quantity=1),
            Resource(name="Laptop for Coding", category="Equipment", image="laptop.jpg", quantity=10),
            Resource(name="PA System", category="Audio", image="pa.jpg", quantity=2),
            Resource(name="Stage Setup", category="Decoration", image="stage.jpg", quantity=1),
            Resource(name="Sound System Premium", category="Audio", image="sound.jpg", quantity=3),
            Resource(name="Power Strips & Extensions", category="Equipment", image="power.jpg", quantity=15),
        ]
        
        # Add to database
        db.session.add_all(events)
        db.session.add_all(resources)
        db.session.commit()
        
        print("✓ Database seeded successfully!")
        print(f"  - {len(events)} events added")
        print(f"  - {len(resources)} resources added")

if __name__ == "__main__":
    seed_database()
