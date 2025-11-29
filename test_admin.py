#!/usr/bin/env python3
"""
Test admin login functionality
"""

from app import create_app
from models import db, User

app = create_app()

with app.app_context():
    # Check if admin exists
    admin = User.query.filter_by(email="admin@college.com", is_admin=True).first()
    
    if admin:
        print("✓ Admin user found in database")
        print(f"  Email: {admin.email}")
        print(f"  Name: {admin.name}")
        print(f"  Is Admin: {admin.is_admin}")
        
        # Test password
        if admin.check_password("admin123"):
            print("✓ Password verification works")
        else:
            print("✗ Password verification failed")
    else:
        print("✗ No admin user found. Run: python seed_data.py")
    
    # List all users
    all_users = User.query.all()
    print(f"\nTotal users in database: {len(all_users)}")
    for user in all_users:
        print(f"  - {user.name} ({user.email}) - Admin: {user.is_admin}")
