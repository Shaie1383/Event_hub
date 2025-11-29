#!/usr/bin/env python3
"""
Test admin login via Flask test client
"""

from app import create_app
from models import db

app = create_app()

with app.test_client() as client:
    print("Testing Admin Login Flow...\n")
    
    # GET admin login page
    print("1. GET /admin/login")
    response = client.get("/admin/login")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✓ Login page accessible")
    
    # POST login credentials
    print("\n2. POST /admin/login (admin@college.com / admin123)")
    response = client.post("/admin/login", data={
        "email": "admin@college.com",
        "password": "admin123"
    }, follow_redirects=True)
    
    print(f"   Status: {response.status_code}")
    
    if "admin_dashboard" in response.request.path or "/admin/dashboard" in response.request.path:
        print("   ✓ Redirected to dashboard")
    elif "Logged in successfully" in response.data.decode():
        print("   ✓ Login successful message found")
    else:
        print(f"   Path: {response.request.path}")
        if "Admin Login" in response.data.decode():
            print("   ✗ Still on login page - authentication failed")
        if "not found" in response.data.decode():
            print("   ✗ Admin not found message")
    
    # Check if session was set
    print("\n3. Checking session after login...")
    response = client.get("/admin/dashboard")
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        print("   ✓ Dashboard accessible (logged in)")
    else:
        print("   ✗ Dashboard not accessible (not logged in)")
    
    print("\nAdmin Login Test Complete!")
