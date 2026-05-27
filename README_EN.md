English | [中文](README.md)

# Student Attendance Management System

A Django-based student attendance web system supporting user registration/login, teacher-generated attendance codes, student code-based check-in, and role-specific management dashboards for administrators, teachers, and students.

## Features

- **Multi-role Management**: Admin (class/user management, CSV batch import), Teacher (attendance code generation, real-time monitoring, Excel export), Student (check-in, history)
- **Secure Authentication**: argon2-cffi password hashing, django-axes brute-force protection, session security
- **Real-time Check-in Monitoring**: Auto-polling every 3 seconds, live display of checked-in / unchecked-in students
- **Excel Attendance Export**: Professional attendance reports via openpyxl
- **CSV Batch Import**: Import classes, students, and teachers in bulk with downloadable templates
- **Audit Logging**: Tracks logins, password changes, data imports, and other security events
- **NTP Time Sync**: Uses Alibaba Cloud NTP server for accurate system time
- **Responsive Design**: Bootstrap 5, compatible with desktop, tablet, and mobile

## Tech Stack

| Category | Technology |
|----------|------------|
| Backend Framework | Python 3.10+ / Django 4.2 LTS |
| Database | SQLite (dev) / MySQL (production) |
| Frontend | HTML5 / CSS3 / ES6 / Bootstrap 5 |
| Password Hashing | argon2-cffi |
| Security | django-axes |
| Excel Export | openpyxl |
| Time Sync | ntplib (ntp.aliyun.com) |

## Quick Start

```bash
# 1. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Configure environment — SQLite works out of the box, no config needed
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# 4. Run database migrations
python manage.py migrate

# 5. Load seed data
python manage.py seed_data

# 6. Start the server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Admin | `admin` | `12345678` |
| Teacher | `teacher1` | `12345678` |
| Student | `student1` | `12345678` |

## Project Structure

```
student-attendance-system/
├── manage.py
├── requirements.txt
├── config/                  # Django project configuration
├── accounts/                # Account management app
├── attendance/              # Attendance check-in app
├── management_app/          # Admin panel app
├── templates/               # HTML templates
├── static/                  # Static assets
├── media/                   # Temporary export files
└── logs/                    # Audit logs
```

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
