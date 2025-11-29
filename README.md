# College Event & Resource System

A lightweight Flask app for managing college events and resources. This project enables students to register for college events and book campus resources through a clean, modern interface with smooth animations. Admins can manage bookings, approve/reject requests, and organize events efficiently.

---

## 🌐 Live Demo

**[View Live Application](https://event-hub-kqqy.onrender.com/events)**

---

## ✨ Features

### 1. **Event Registration System**
- Browse all college events with search and filter options
- View detailed event information (date, location, description, team size, fee)
- AJAX-based registration modal for seamless registration
- Support for multi-part events (e.g., Ripples has Technical & Non-Technical)
- Responsive event cards with images and event metadata

### 2. **Resource Booking System**
- Browse available campus resources (projectors, mics, lights, halls, etc.)
- Advanced booking modal with date range selection
- Automatic conflict detection to prevent double-booking
- Smart resource suggestions based on event type
- Support for 10+ different resource categories

### 3. **Admin Dashboard**
- Session-based admin authentication
- View all pending resource bookings and event registrations
- Approve or reject resource booking requests
- Manage resource availability and status
- Real-time dashboard with pending actions count

### 4. **Modern UI/UX**
- Glassmorphism dark theme with neon blue accents
- Bootstrap 5 responsive grid layout
- AOS scroll animations for visual polish
- Mobile-friendly interface
- Smooth modal transitions and form interactions

---

## 📁 Project Structure

```
college_event_system/
├── app.py                      # Flask app factory & entrypoint
├── config.py                   # Configuration settings
├── models.py                   # SQLAlchemy database models
├── seed_data.py                # Database seeding script
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker container config
├── Procfile                    # Render deployment config
├── .gitignore                  # Git ignore rules
├── blueprints/
│   ├── events.py              # Events routes & logic
│   ├── resources.py           # Resources routes & logic
│   └── admin.py               # Admin routes & dashboard
├── templates/
│   ├── base.html              # Base template with navbar
│   ├── home.html              # Landing page
│   ├── events.html            # Events listing page
│   ├── event_detail.html      # Single event detail page
│   ├── resources.html         # Resources listing & suggestions
│   ├── admin_login.html       # Admin login form
│   └── admin_dashboard.html   # Admin dashboard
├── static/
│   ├── css/custom.css         # Custom dark theme styling
│   ├── js/custom.js           # JavaScript utilities
│   └── img/                   # Event & resource images
└── app_data.db               # SQLite database (auto-created)
```

---

## 📊 Demo Data

### Events (5 Pre-seeded)
- **Ripples 2024** - Main annual cultural event with Technical & Non-Technical sub-events
- **Tech Expo 2024** - Technology exhibition and workshops
- **Code Hackathon 2024** - 24-hour coding competition
- **Freshers Party 2024** - Welcome event for first-year students
- **DJ Night** - Evening music and dance event

### Resources (10 Pre-seeded)
- **Audio**: Wireless Microphone System, PA System, Sound System
- **AV**: Projector (HD), Projector Screen
- **Decoration**: LED Lights Kit, Stage Setup
- **Hall**: Main Hall (1 available)
- **Equipment**: Laptop Stand, Power Strips (8-outlet)

### Admin Account (Pre-seeded)
```
Email: admin@college.com
Password: admin123
```

---

## 🚀 Quick Start (Local)

### Prerequisites
- Python 3.8+
- pip package manager

### Installation & Run (5 minutes)

1. **Clone and navigate to project:**
   ```powershell
   cd "c:\Users\shais\Desktop\register & resources\college_event_system"
   ```

2. **(Optional) Create virtual environment:**
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Start the application:**
   ```powershell
   python app.py
   ```
   *or*
   ```powershell
   python -m flask run
   ```

5. **Access in browser:**
   - Home: http://127.0.0.1:5000/
   - Events: http://127.0.0.1:5000/events
   - Resources: http://127.0.0.1:5000/resources
   - Admin: http://127.0.0.1:5000/admin/login

**Note**: Database is auto-seeded on first run. No manual setup needed!

---

## 🗄️ Database Models

### User
- `id` (Primary Key)
- `name`, `email` (unique)
- `password_hash` (bcrypt hashed)
- `is_admin` (boolean)
- Relationships: registrations, bookings

### Event
- `id` (Primary Key)
- `title`, `category`, `date`, `location`
- `image`, `description_short`, `description_long`
- `team_size`, `fee`
- Relationships: registrations

### Resource
- `id` (Primary Key)
- `name`, `category`, `image`, `quantity`
- Relationships: bookings

### Registration
- `id` (Primary Key)
- `event_id` (Foreign Key), `user_id` (Foreign Key)
- `name`, `registration_no`, `email`, `mobile`
- `branch`, `year`, `created_at`

### Booking
- `id` (Primary Key)
- `resource_id` (Foreign Key), `user_id` (Foreign Key)
- `event_name`, `purpose`
- `start_date`, `end_date`
- `status` (pending/approved/rejected), `created_at`

---

## 🔑 API Endpoints

### Events Blueprint (`/events`)
- `GET /events` - List all events (supports filtering)
- `GET /event/<id>` - Event detail page
- `GET /api/event/<id>` - Event data (JSON)
- `POST /register-event` - Submit event registration

### Resources Blueprint (`/resources`)
- `GET /resources` - List all resources (supports filtering)
- `GET /api/resources/suggestions` - Get resource suggestions
- `POST /book-resource` - Submit resource booking

### Admin Blueprint (`/admin`)
- `GET /admin/login` - Admin login form
- `POST /admin/login` - Process login (session-based)
- `GET /admin/dashboard` - View pending bookings & registrations
- `POST /api/approve-booking` - Approve booking
- `POST /api/reject-booking` - Reject booking

---

## 👥 User Journeys

### Event Registration Flow
1. Visit `/events` page
2. Browse event cards or use search/filter
3. Click "View More" on event card
4. See full event details at `/event/<id>`
5. Click "Register" button
6. Fill registration form in modal (name, email, branch, year, etc.)
7. Click "Submit"
8. Success message displayed

### Resource Booking Flow
1. Visit `/resources` page
2. Browse resource cards or filter by category
3. See suggested resources for different event types
4. Click "Book" on desired resource
5. Fill booking form (select dates, event name, purpose, personal info)
6. System checks for date conflicts
7. Click "Submit"
8. Success message and admin notification sent
9. Admin reviews and approves/rejects at `/admin/dashboard`

---

## 🛠️ Tech Stack

- **Backend**: Flask 3.0.2, Flask-SQLAlchemy 3.1.1, Flask-Migrate 4.0.5
- **Database**: SQLite (development), PostgreSQL (production-ready)
- **Frontend**: Bootstrap 5, Jinja2 templates, Vanilla JavaScript, AJAX
- **Styling**: Custom CSS (glassmorphism theme), AOS animations
- **Deployment**: Docker, Gunicorn, GitHub Actions CI/CD
- **Hosting**: Render.com (free tier)

---

## 🚢 Deployment

### Deploy to Render (Recommended)

1. **Push to GitHub:**
   ```powershell
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/<username>/<repo>.git
   git push -u origin main
   ```

2. **On Render.com:**
   - Click "New" → "Web Service"
   - Connect your GitHub repository
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn app:app`
   - Click "Create Web Service"

3. **Database**: 
   - SQLite works for demo (auto-seeded)
   - For production, use Render's PostgreSQL add-on and set `DATABASE_URL` env var

### Docker (Local Testing)
```powershell
docker build -t college-event-system .
docker run -p 5000:5000 college-event-system
```

### Environment Variables
- `FLASK_ENV`: `production` or `development`
- `DATABASE_URL`: PostgreSQL connection string (optional)
- `SECRET_KEY`: Flask session secret (auto-generated if not set)

---

## ⚙️ Configuration

Edit `config.py` to customize:
- Database location (`SQLALCHEMY_DATABASE_URI`)
- Session timeout and secret key
- Debug and testing modes

---

## 🔐 Admin Features

### Create Additional Admin Users

Via Python shell:
```python
from app import create_app
from models import db, User

app = create_app()
with app.app_context():
    admin = User(name="New Admin", email="admin2@college.com", is_admin=True)
    admin.set_password("securepassword")
    db.session.add(admin)
    db.session.commit()
```

### Admin Dashboard Tasks
- View all pending resource bookings
- View all event registrations
- Approve resource bookings (changes status to "approved")
- Reject resource bookings (changes status to "rejected")
- Track booking dates and user information

---

## 🎯 Editing Event & Resource Data

### Option 1: Edit Seed File
- File: `seed_data.py`
- Modify the event/resource lists in the `events = [...]` and `resources = [...]` sections
- Delete `app_data.db` and re-run `python seed_data.py`

### Option 2: Use Flask Shell (Recommended for Single Changes)
```powershell
python
>>> from app import create_app
>>> app = create_app()
>>> from models import db, Event
>>> ctx = app.app_context(); ctx.push()
>>> event = Event.query.filter_by(title="Ripples 2024").first()
>>> event.location = "New Venue"
>>> event.fee = 500
>>> db.session.commit()
>>> ctx.pop()
```

---

## 🧪 Testing & Troubleshooting

### Issue: No events or resources shown
**Solution**: Database auto-seeds on startup. If missing data:
```powershell
python seed_data.py
```

### Issue: Admin login fails
**Solution**: Re-seed the database:
```powershell
python seed_data.py
```
Or create admin via Flask shell (see "Creating Additional Admins" above)

### Issue: Port 5000 already in use
**Solution**: Change port when running:
```powershell
python -m flask run --port 5001
```

### Issue: Static images not loading
**Solution**: Ensure images exist in `static/img/` folder with exact names referenced in seed data.

---

## 📚 Stack Overflow & References

- Flask Documentation: https://flask.palletsprojects.com/
- SQLAlchemy ORM: https://docs.sqlalchemy.org/
- Bootstrap 5: https://getbootstrap.com/docs/5.0/
- AOS Animations: https://michalsnik.github.io/aos/
- Render Deployment: https://render.com/docs

---

## 📋 Requirements

See `requirements.txt`:
- Flask==3.0.2
- Flask-SQLAlchemy==3.1.1
- Flask-Migrate==4.0.5
- gunicorn==21.2.0
- python-dotenv==1.0.0
- Jinja2==3.1.2
- Werkzeug==3.0.1
- Flask-Login==0.6.3
- blinker==1.7.0

---

## 🎨 Design Highlights

- **Dark Glassmorphism Theme**: Semi-transparent frosted glass effect with backdrop blur
- **Neon Blue Accents**: #60A5FA primary color for CTAs and highlights
- **Smooth Animations**: AOS scroll animations (fade, zoom, slide) on all pages
- **Responsive Design**: Mobile-first Bootstrap 5 grid (works on phones, tablets, desktops)
- **Modal Forms**: Smooth AJAX-based registration and booking modals

---

## 📝 Customization Tips

1. **Change Colors**: Edit `static/css/custom.css` - look for `#60A5FA` (neon blue)
2. **Add Events**: Modify `seed_data.py` and re-seed
3. **Upload Images**: Place images in `static/img/` and reference in seed data
4. **Change Navbar**: Edit `templates/base.html`
5. **Modify Database Fields**: Edit `models.py` and run `flask db migrate`

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Shaista** - College Event & Resource Booking System

- 🔗 GitHub: [Shaie1383](https://github.com/Shaie1383)
- 🌐 Live Demo: [event-hub-kqqy.onrender.com](https://event-hub-kqqy.onrender.com)

---

## ✅ Status & Next Steps

**Completed**:
- ✅ Full event management system with registration
- ✅ Resource booking with conflict detection
- ✅ Admin dashboard with approval workflow
- ✅ Responsive dark theme UI
- ✅ Database auto-initialization
- ✅ GitHub Actions CI/CD pipeline
- ✅ Live deployment on Render

**Suggested Future Enhancements**:
- 📧 Email notifications for booking approvals
- 📸 Image upload feature for admins
- 📱 Mobile app (React Native)
- 🔔 Real-time notifications (WebSocket)
- 💳 Payment integration for event fees
- 📊 Admin analytics dashboard
- 🔍 Advanced search with filters
- 🗓️ Calendar view for events

---

**Last Updated**: December 2024  
**Status**: Production-Ready ✅

For questions or issues, please open a GitHub issue or contact the author.
