# College Event & Resource System

A lightweight Flask app for managing college events and resources (demo-ready).

This project is a web application that allows students to register for college events and book campus resources easily. It provides a clean, modern interface with smooth animations and event details. Students can register for technical and non-technical events, while admins can manage bookings and approve or reject requests. The system makes event handling and resource allocation faster, clearer, and more organized.

<!--- Combined README: Quickstart + Final Status + Admin Guide --->
# College Event & Resource System

A single-file documentation for the College Event & Resource System — a lightweight Flask application for managing college events, registrations, and resource bookings. This README consolidates setup, features, admin instructions, deployment notes, and troubleshooting into a single reference.

---

## Key Links

- Home (local): `http://127.0.0.1:5000/`
- Events: `http://127.0.0.1:5000/events`
- Resources: `http://127.0.0.1:5000/resources`
- Admin Login: `http://127.0.0.1:5000/admin/login`

---

## Quickstart — Run locally (5 minutes)

1. Open a PowerShell terminal and go to the project folder:

```powershell
cd "c:/Users/shais/Desktop/register & resources/college_event_system"
```

2. (Optional) Create & activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Seed the database (one-time):

```powershell
python seed_data.py
```

5. Run the app:

```powershell
python app.py
# or
python -m flask run
```

6. Open `http://127.0.0.1:5000` in your browser.

Admin test credentials (seeded):

```
Email: admin@college.com
Password: admin123
```

---

## Project Overview & Structure

Top-level files you will work with:

- `app.py` — Flask app factory / entrypoint
- `config.py` — configuration (env override)
- `models.py` — database models (`Event`, `Resource`, `User`, `Registration`, `Booking`)
- `seed_data.py` — creates sample events, resources, and an admin user
- `requirements.txt` — Python dependencies
- `Dockerfile`, `Procfile` — helpers for containerized or Procfile-based deploys

Key folders:

- `blueprints/` — `events.py`, `resources.py`, `admin.py` (routing & view logic)
- `templates/` — Jinja2 templates (UI)
- `static/` — `css/`, `js/`, `img/` (assets)

If you plan to push to GitHub, keep `venv/` out of version control (see `.gitignore`).

---

## What’s Included (Features)

- Event listing, detail pages, and AJAX registration modal
- Resource listing, booking modal, date-range booking, conflict detection
- Admin dashboard: view/approve/reject bookings and view registrations
- Seed script with 5 sample events and 10 resources
- Responsive dark theme with Bootstrap and AOS animations

---

## How to Edit Event Details (date, location, fee, image)

You can change event data in two ways:

- Edit the seed file (for sample data):
  - File: `seed_data.py`
  - Modify the `events = [ Event(...), ... ]` block and either delete `app_data.db` and re-run `python seed_data.py`, or manually update the record in the DB.

- Update an existing record in the running app using the Flask shell (recommended for single edits):

```powershell
python
>>> from app import create_app
>>> app = create_app()
>>> from models import db, Event
>>> ctx = app.app_context(); ctx.push()
>>> e = Event.query.filter_by(title="Ripples 2024").first()
>>> e.location = "New Location"
>>> from datetime import datetime
>>> e.date = datetime(2025, 12, 22).date()
>>> db.session.commit()
>>> ctx.pop()
```

Notes:
- The `Event` model (in `models.py`) defines the available fields: `title`, `category`, `date`, `location`, `image`, `description_short`, `description_long`, `team_size`, `fee`.
- If you change the category for an event (e.g., set `category="Ripples"`), specific UI logic that shows sub-events may trigger (see `blueprints/events.py`).

---

## Admin Dashboard (login & common tasks)

Admin login page: `http://127.0.0.1:5000/admin/login`

Seeded admin credentials:

```
Email: admin@college.com
Password: admin123
```

After login you can:

- View pending bookings and registrations
- Approve/Reject resource bookings
- Manage resources (add/edit/delete)
- View all events and registrations

Create additional admins via the Flask shell (example in `ADMIN_LOGIN_GUIDE.md` before it was consolidated):

```python
from app import create_app
from models import db, User

app = create_app()
with app.app_context():
    admin = User(name="New Admin", email="admin2@college.com", is_admin=True)
    admin.set_password("newpassword")
    db.session.add(admin)
    db.session.commit()

```

---

## Deployment — recommended platforms & quick steps

This app runs as a standard Flask app and can be deployed in many ways. For production use a managed Postgres database instead of SQLite.

Recommended platforms (easy → advanced):

- Render (easy): GitHub → Render Web Service, set build command `pip install -r requirements.txt` and start command `gunicorn app:app`.
- Railway: GitHub → Railway project, add Postgres plugin, set start `gunicorn app:app`.
- Fly.io: container-first (use `Dockerfile` and `flyctl deploy`).
- Google Cloud Run / Azure Web App for Containers: build & push container, deploy to managed serverless container.

Quick Git + Render workflow:

```powershell
cd "c:/Users/shais/Desktop/register & resources/college_event_system"
git init
git add .
git commit -m "Initial commit"
# create repo on GitHub and add remote
git remote add origin https://github.com/<you>/<repo>.git
git push -u origin main

# On Render: New → Web Service → Connect Repo → Deploy
```

Docker (local test):

```powershell
docker build -t college-event-system .
docker run -p 5000:5000 college-event-system
```

Environment variables to set on production:
- `DATABASE_URL` — (Postgres) connection string
- `FLASK_ENV` — `production`
- Any secret keys / config in `config.py` or env

If you want I can add a small `config.py` loader that prefers `DATABASE_URL` when present.

---

## Troubleshooting

- No events shown: run `python seed_data.py` or delete `app_data.db` and re-seed.
- Admin login fails: re-run `python seed_data.py` to recreate admin or create one via Flask shell.
- Port in use: change host/port when running or stop existing process.

If you see template or routing errors, check `blueprints/events.py` for `url_for` endpoint names and `templates/` for matching names.

---

## Project Status (summary)

- Development-ready, demoable with seeded data (5 events, 10 resources).
- Admin functionality and booking approval workflow implemented.
- Suggested next steps before production: migrate to Postgres, add email notifications, add image upload, and secure admin endpoints.

---

## Credit

Crafted with 💙 by Shaista — consolidated README.

- ✅ Events page displays all event cards with:
  - Event image, title, date, location
  - Short description
  - "View More" button (navigates to /event/<id>)
  - "Register" button (opens modal form)
- ✅ Event detail page shows:
  - Full event information
  - Large description
  - Registration modal popup
  - AJAX form submission to `/register-event`
- ✅ Database seeded with 5 sample events:
  - Ripples 2024 (Non-Technical)
  - Code Hackathon 2024 (Hackathons)
  - Tech Expo 2024 (Workshops)
  - Freshers Party 2024 (Non-Technical)
  - DJ Night (Non-Technical)

### 2. **Resource Booking System**
- ✅ Resources page displays all resource cards with:
  - Resource image, name, category, quantity
  - Smart "Best for" suggestions per resource type
  - "Book" button (opens booking modal)
- ✅ Booking modal form collects:
  - Personal info (name, registration no, email, mobile)
  - Academic info (branch, year)
  - Booking details (start date, end date, event name, purpose)
  - AJAX submission to `/book-resource`
- ✅ Database seeded with 10 sample resources:
  - Wireless Microphone System (Audio)
  - Projector HD (AV)
  - LED Lights Kit (Decoration)
  - Main Hall (Hall)
  - PA System (Audio)
  - And 5 more...

### 3. **Event-Specific Resource Suggestions**
- ✅ Bottom of resources page displays 3 suggestion categories:
  1. **🎯 For Ripples Events**: Wireless Mic, Projector, Decoration Lights, Main Hall
  2. **💻 For Technical Events**: Laptops, Projector Screen, PA System, Power Strips
  3. **🎭 For Cultural Events**: Sound System, Stage Lights, Decoration Items, Chairs & Tables
- ✅ Each suggestion shown with emoji icons and labels

### 4. **Database & Models**
- ✅ SQLite database (app_data.db) with tables:
  - User (admin accounts)
  - Event (event information)
  - Resource (resource inventory)
  - Registration (event registrations)
  - Booking (resource bookings)
- ✅ Relationships properly configured with backrefs
- ✅ 5 events + 10 resources seeded successfully

### 5. **Frontend UI/UX**
- ✅ Glassmorphism dark theme with Bootstrap 5
- ✅ AOS scroll animations on all pages
- ✅ Modal popups for registration and booking
- ✅ Responsive grid layout (mobile-friendly)
- ✅ Filter/search bars on events and resources pages
- ✅ Consistent neon blue (#60A5FA) accent color

### 6. **Backend API Endpoints**
- ✅ Events Blueprint:
  - `GET /events` - List all events with filters
  - `GET /event/<id>` - Event detail page
  - `POST /register-event` - Register for event
  - `GET /api/event/<id>` - Event JSON data
- ✅ Resources Blueprint:
  - `GET /resources` - List all resources with filters
  - `POST /book-resource` - Book a resource
  - `GET /api/resources/suggestions` - Get suggestions
- ✅ Admin Blueprint:
  - `GET /admin/login` - Admin login form
  - `POST /admin/login` - Process login
  - `GET /admin/dashboard` - View pending bookings
  - `GET /admin/booking/<id>/approve` - Approve booking
  - `GET /admin/booking/<id>/reject` - Reject booking

---

## 🎯 User Journey

### **Event Registration Flow**
1. User visits `/events` page
2. Browse all event cards OR filter by category/search
3. Click "View More" → sees full event details at `/event/<id>`
4. Click "Register" button → modal popup appears
5. Fill registration form (name, registration no, email, etc.)
6. Click "Submit" → AJAX POST to `/register-event`
7. Success message → registration saved to database

### **Resource Booking Flow**
1. User visits `/resources` page
2. Browse all resource cards OR filter by category
3. See event-specific suggestions at bottom
4. Click "Book" button on resource → modal popup appears
5. Fill booking form (dates, event name, purpose, personal info)
6. Click "Submit" → AJAX POST to `/book-resource`
7. Success message → booking saved to database
8. Admin can approve/reject at `/admin/dashboard`

---

## 📁 Project Structure

```
college_event_system/
├── app.py                    # Main Flask app
├── config.py                # Configuration
├── models.py               # Database models
├── seed_data.py            # Database seeding script
├── requirements.txt        # Dependencies
├── blueprints/
│   ├── events.py          # Events routes
│   ├── resources.py       # Resources routes
│   └── admin.py           # Admin routes
├── templates/
│   ├── base.html          # Base template with navbar
│   ├── home.html          # Landing page
│   ├── events.html        # Events listing + registration modal
│   ├── event_detail.html  # Single event detail + modal
│   ├── resources.html     # Resources listing + booking modal + suggestions
│   └── admin_*.html       # Admin templates
├── static/
│   ├── css/custom.css     # Custom dark theme styling
│   ├── js/custom.js       # JavaScript utilities
│   └── img/               # Image placeholder directory
└── app_data.db           # SQLite database (auto-created)
```

---

## 🚀 How to Run

1. **Start the Flask server:**
   ```bash
   cd "c:/Users/shais/Desktop/register & resources/college_event_system"
   python -m flask run
   ```

2. **Access the application:**
   - Home: http://127.0.0.1:5000/
   - Events: http://127.0.0.1:5000/events
   - Resources: http://127.0.0.1:5000/resources
   - Admin Login: http://127.0.0.1:5000/admin/login

3. **Database already seeded** with sample data (5 events + 10 resources)

---

## 📝 Sample Data

### Events (Seeded)
- Ripples 2024 - Main cultural event
- Code Hackathon 2024 - 24-hour coding competition
- Tech Expo 2024 - Technology exhibition & workshops
- Freshers Party 2024 - Welcome event
- DJ Night - Evening music & dance

### Resources (Seeded)
- Audio: Wireless Mic, PA System, Sound System
- AV: Projector, Projection Screen
- Decoration: LED Lights, Stage Setup
- Hall: Main Hall (1 available)
- Equipment: Laptops, Power Strips

---

## ✨ Key Features Implemented

| Feature | Status | Details |
|---------|--------|---------|
| Event Listing | ✅ | Display cards with filters |
| Event Registration Modal | ✅ | Pop-up form with AJAX submit |
| Resource Listing | ✅ | Display cards with filters |
| Resource Booking Modal | ✅ | Pop-up form with AJAX submit |
| Event Suggestions | ✅ | Show resources for each event type |
| Database Seeding | ✅ | 5 events + 10 resources |
| Admin Dashboard | ✅ | View & approve/reject bookings |
| Responsive Design | ✅ | Mobile-friendly with Bootstrap 5 |
| Dark Theme | ✅ | Glassmorphism with neon accents |
| Scroll Animations | ✅ | AOS animations on all pages |

---

## 🔐 Admin Access

The system uses session-based authentication (development mode only).

- Admin credentials can be created via database
- Admin dashboard at `/admin/login`
- Approve/reject resource bookings
- View all registrations

---

## 🎨 Styling & Theme

- **Color Scheme**: Dark glassmorphism (rgba backgrounds, backdrop-filter blur)
- **Primary Accent**: Neon Blue (#60A5FA)
- **Typography**: Modern sans-serif
- **Animations**: AOS scroll effects (fade, zoom, slide)
- **Responsive**: Mobile-first Bootstrap 5 grid

---

## 📊 Database Schema

### Event Table
- id (PK)
- title, category, date, location
- image, description_short, description_long
- team_size, fee

### Resource Table
- id (PK)
- name, category
- image, quantity

### Registration Table
- id (PK)
- event_id (FK), user_id (FK)
- name, regno, email, mobile, year
- created_at

### Booking Table
- id (PK)
- resource_id (FK), user_id (FK)
- event_name, purpose
- start_date, end_date, status
- created_at

---

**Last Updated**: 27 Nov 2025
**Status**: ✅ All features completed and tested
