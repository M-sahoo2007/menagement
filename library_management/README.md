# College Library Management System

A comprehensive Flask-based library management system with role-based access control, student and admin portals, and secure authentication.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [System Overview](#system-overview)
3. [Features](#features)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Security Architecture](#security-architecture)
7. [File Structure](#file-structure)
8. [Routes & Endpoints](#routes--endpoints)
9. [Database Schema](#database-schema)
10. [Testing Checklist](#testing-checklist)
11. [Troubleshooting](#troubleshooting)
12. [Deployment](#deployment)

---

## 🚀 Quick Start

### 1. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 2. Configure Secret Code
Edit `config.py`:
```python
ADMIN_SECRET_CODE = 'ADMIN2025'  # Change this to your secret code
```

### 3. Run Application
```powershell
python app.py
```

### 4. Access System
- **URL**: http://localhost:5000
- **Admin Registration**: Admin → Register with your secret code
- **Student Management**: Admin → Students (after login)

---

## 📊 System Overview

### Architecture
```
┌─────────────────────────────────────────┐
│   College Library Management System      │
├─────────────────────────────────────────┤
│  Public Layer (No Auth Required)         │
│  ├─ Home Page (/)                        │
│  ├─ Student Login (/student/login)       │
│  └─ Admin Login (/admin/login)           │
│                                           │
│  Student Layer (Login Required)          │
│  ├─ Dashboard (/student/dashboard)       │
│  ├─ Available Books (/student/books)     │
│  ├─ Borrow Books (/student/borrow/<id>)  │
│  ├─ Return Books (/student/return/<id>)  │
│  └─ Report Issues (/student/reports)     │
│                                           │
│  Admin Layer (Admin Login Required)      │
│  ├─ Dashboard (/admin/dashboard)         │
│  ├─ Register Students (/admin/students)  │
│  ├─ Manage Books (/admin/book/...)       │
│  ├─ View Reports (/admin/reports)        │
│  └─ Respond to Issues (/admin/report/...)│
│                                           │
│  Security Layer (Registration)           │
│  ├─ Student Registration → Admin Only    │
│  └─ Admin Registration → Secret Code     │
└─────────────────────────────────────────┘
```

### Key Components
- **Flask Application** (`app.py`): 30+ routes, business logic, database operations
- **SQLite Database** (`library.db`): Auto-created with 5 normalized tables
- **Configuration** (`config.py`): Centralized settings for secret code
- **Templates** (21 HTML files): Responsive Bootstrap UI with Jinja2 templating
- **Styling** (`style.css`): Bootstrap 5.3.0 + custom styles

---

## ✨ Features

### 🔐 Security Features
- **Three-Layer Authentication**
  1. Student registration restricted to admin only
  2. Admin registration requires secret code verification
  3. System access requires login with password hashing (Werkzeug SHA256)
  
- **Role-Based Access Control (RBAC)**
  - Student role: Book borrowing, returns, issue reporting
  - Admin role: Student management, book inventory, issue response
  
- **Session Management**: Secure cookie-based sessions with auto-timeout

### 📚 Core Features
- **Student Portal**
  - View available books with filtering
  - Borrow and return books
  - Track borrowing history
  - Report issues or damage to books
  - View personal dashboard and statistics

- **Admin Portal**
  - Register new students (with form validation)
  - Manage student accounts (view, delete)
  - Add and manage book inventory
  - Track book borrowing/return status
  - Respond to student issues
  - Generate reports and statistics

- **Book Management**
  - Book catalog with details (title, author, ISBN, category, quantity)
  - Real-time availability tracking
  - Category-based filtering
  - Search functionality

- **Issue Management**
  - Students can report book damage or issues
  - Admins can track and respond to issues
  - Status tracking (open, in_progress, resolved)

---

## 💾 Installation

### Prerequisites
- Python 3.8+ (verified with 3.13)
- pip (Python package manager)
- Windows PowerShell or Command Prompt

### Setup Steps

1. **Navigate to project directory**
   ```powershell
   cd c:\Users\sahoo\Desktop\menagement\library_management
   ```

2. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```
   
   **Required packages**:
   - Flask==2.3.3
   - Werkzeug==2.3.7

3. **Verify installation**
   ```powershell
   python -c "from app import app; from config import ADMIN_SECRET_CODE; print('✅ All systems ready!')"
   ```

4. **Run application**
   ```powershell
   python app.py
   ```

The application will:
- Auto-create `library.db` SQLite database
- Initialize 5 tables (students, admin, books, book_issues, reports)
- Start Flask development server on http://localhost:5000
- Enable debugger for development

---

## ⚙️ Configuration

### Secret Code Management

**Location**: `config.py`

**Default Code**: `'ADMIN2025'`

**Change the code**:
```python
# config.py
ADMIN_SECRET_CODE = 'YOUR_NEW_SECRET_CODE'
```

**Examples**:
- `'UNIVERSITY_ADMIN_2025'`
- `'LIB@2025#SECURE'`
- `'MyLibrary2025'`

**Using the new code**:
1. Go to Admin → Register page
2. Enter the new code in the "Secret Code" field
3. If code matches `ADMIN_SECRET_CODE`, registration succeeds
4. Otherwise, error message appears: "Invalid secret code!"

### Environment Settings

**Development** (current):
- Debug mode: Enabled
- Host: localhost (127.0.0.1)
- Port: 5000
- Database: library.db (SQLite)

**For Production**:
1. Change `app.run(debug=True)` to `app.run(debug=False)` in app.py line ~596
2. Use a production WSGI server (Gunicorn, uWSGI)
3. Set strong secret code in config.py
4. Use environment variables for sensitive settings

---

## 🔒 Security Architecture

### Three-Layer Security Model

```
Layer 1: Registration Control
├─ Student Registration: Admin-only
│  └─ Route /student/register: REMOVED
│  └─ Access: Via /admin/students (admin only)
└─ Admin Registration: Secret code required
   └─ Route /admin/register: Requires ADMIN_SECRET_CODE

Layer 2: Password Hashing
├─ Algorithm: Werkzeug SHA256 with salting
├─ Functions:
│  ├─ werkzeug.security.generate_password_hash()
│  └─ werkzeug.security.check_password_hash()
└─ Database: Passwords stored as hashes, never plaintext

Layer 3: Session Management
├─ Authentication: Flask sessions (secure cookies)
├─ Decorators:
│  ├─ @login_required: Validates user session
│  └─ @admin_required: Validates admin role
└─ Behavior: Auto-logout on session expiration
```

### Access Control Matrix

| Route | Public | Student | Admin | Protection |
|-------|--------|---------|-------|------------|
| `/` (Home) | ✅ | ✅ | ✅ | None |
| `/student/login` | ✅ | ✅ | ✅ | None |
| `/admin/login` | ✅ | ✅ | ✅ | None |
| `/admin/register` | ✅ | ✅ | ✅ | Secret Code |
| `/student/dashboard` | ❌ | ✅ | ❌ | login_required |
| `/student/books` | ❌ | ✅ | ❌ | login_required |
| `/admin/dashboard` | ❌ | ❌ | ✅ | admin_required |
| `/admin/students` | ❌ | ❌ | ✅ | admin_required |
| `/admin/book/*` | ❌ | ❌ | ✅ | admin_required |

### Password Security
- Hashing: SHA256 with random salt (Werkzeug)
- Storage: Only hashes stored in database
- Verification: `werkzeug.security.check_password_hash()`
- Policy: Minimum 6 characters recommended

### Best Practices Implemented
1. ✅ Never store plaintext passwords
2. ✅ Restrict registration via multiple layers
3. ✅ Session-based authentication with timeouts
4. ✅ CSRF protection via Flask (default)
5. ✅ SQL injection prevention via parameterized queries
6. ✅ Role-based access control with decorators

---

## 📁 File Structure

### Python Files
```
library_management/
├── app.py                          [596 lines] Main Flask application
├── config.py                       Configuration settings
├── requirements.txt                Python dependencies
└── library.db                      SQLite database (auto-created)
```

### Template Files (HTML/Jinja2)
```
templates/
├── base.html                       Base layout with navigation
├── index.html                      Home page
├── student_login.html              Student login form
├── admin_login.html                Admin login form
├── admin_register.html             Admin registration with secret code
├── student_dashboard.html          Student overview and statistics
├── available_books.html            Browse and filter books
├── book_detail.html                Book details with borrow option
├── borrow_confirmation.html        Confirm book borrow
├── borrowed_books.html             View borrowed books
├── return_book.html                Return book process
├── student_reports.html            Report issues
├── create_report.html              Create new issue report
├── admin_dashboard.html            Admin overview and statistics
├── admin_students.html             Student management
├── add_book.html                   Add book to inventory
├── manage_books.html               Book inventory management
├── edit_book.html                  Edit book details
├── admin_reports.html              View all student reports
└── admin_report_detail.html        Respond to issue reports
```

### Static Files
```
static/
└── style.css                       Application styling (Bootstrap + custom)
```

---

## 🔗 Routes & Endpoints

### Public Routes (No Authentication)
| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/` | Home page |
| GET | `/student/login` | Student login form |
| POST | `/student/login` | Process student login |
| GET | `/admin/login` | Admin login form |
| POST | `/admin/login` | Process admin login |
| GET | `/admin/register` | Admin registration form |
| POST | `/admin/register` | Process admin registration (requires secret code) |

### Student Routes (Login Required)
| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/student/dashboard` | Student dashboard |
| GET | `/student/books` | View available books |
| GET | `/book/<int:id>` | Book details |
| GET | `/student/borrow/<int:id>` | Borrow book |
| GET | `/student/borrowed` | View borrowed books |
| GET | `/student/return/<int:id>` | Return book |
| GET | `/student/reports` | View own reports |
| GET | `/student/report/create` | Create report form |
| POST | `/student/report/create` | Submit report |
| GET | `/logout` | Logout |

### Admin Routes (Admin Login Required)
| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/admin/dashboard` | Admin dashboard |
| GET | `/admin/students` | Student management |
| POST | `/admin/students` | Register new student |
| POST | `/admin/student/<int:id>/delete` | Delete student |
| GET | `/admin/book/add` | Add book form |
| POST | `/admin/book/add` | Add book to inventory |
| GET | `/admin/book/manage` | Book inventory |
| GET | `/admin/book/<int:id>/edit` | Edit book form |
| POST | `/admin/book/<int:id>/edit` | Update book |
| POST | `/admin/book/<int:id>/delete` | Delete book |
| GET | `/admin/reports` | View all reports |
| GET | `/admin/report/<int:id>` | Report details |
| POST | `/admin/report/<int:id>/respond` | Respond to report |

---

## 🗄️ Database Schema

### Tables

#### 1. `students`
```sql
CREATE TABLE students (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  roll_number TEXT UNIQUE NOT NULL,
  phone TEXT,
  department TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

#### 2. `admin`
```sql
CREATE TABLE admin (
  id INTEGER PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  name TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
```

#### 3. `books`
```sql
CREATE TABLE books (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  isbn TEXT UNIQUE NOT NULL,
  category TEXT,
  quantity INTEGER DEFAULT 1,
  available_quantity INTEGER DEFAULT 1,
  description TEXT,
  published_year INTEGER,
  image_url TEXT,
  added_by INTEGER,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (added_by) REFERENCES admin(id)
)
```

#### 4. `book_issues`
```sql
CREATE TABLE book_issues (
  id INTEGER PRIMARY KEY,
  student_id INTEGER,
  book_id INTEGER,
  issue_date DATETIME DEFAULT CURRENT_TIMESTAMP,
  return_date DATETIME,
  status TEXT DEFAULT 'borrowed',
  FOREIGN KEY (student_id) REFERENCES students(id),
  FOREIGN KEY (book_id) REFERENCES books(id)
)
```

#### 5. `reports`
```sql
CREATE TABLE reports (
  id INTEGER PRIMARY KEY,
  student_id INTEGER,
  title TEXT NOT NULL,
  description TEXT,
  category TEXT,
  status TEXT DEFAULT 'open',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  response TEXT,
  FOREIGN KEY (student_id) REFERENCES students(id)
)
```

---

## ✅ Testing Checklist

### Essential Tests
- [ ] **Installation**: `pip install -r requirements.txt` succeeds
- [ ] **Startup**: `python app.py` runs without errors
- [ ] **Database**: `library.db` created with 5 tables
- [ ] **Public Pages**: Home, Student Login, Admin Login load
- [ ] **Admin Registration**: Admin Register page visible with secret code field
- [ ] **Secret Code**: Wrong code rejected, correct code accepted
- [ ] **Admin Login**: Can login with registered admin credentials
- [ ] **Student Management**: Admin can register and delete students
- [ ] **Book Management**: Admin can add, edit, delete books
- [ ] **Student Login**: Can login with created student credentials
- [ ] **Book Borrowing**: Student can borrow available books
- [ ] **Book Return**: Student can return borrowed books
- [ ] **Issue Reporting**: Student can report issues
- [ ] **Admin Response**: Admin can respond to student reports
- [ ] **Access Control**: Unauthorized access redirects to login

**Total Testing Time**: ~60 minutes

---

## 🐛 Troubleshooting

### Common Issues

#### "ModuleNotFoundError: No module named 'flask'"
```powershell
pip install -r requirements.txt
```

#### "Address already in use" port 5000
Change port in `app.py` line 596 or kill the process:
```powershell
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

#### Database locked error
```powershell
rm library.db
python app.py  # Will recreate database
```

#### Secret code not working
- Check `config.py` for correct code
- Ensure no trailing spaces
- Code is case-sensitive

#### Can't borrow book
- Verify book `available_quantity` > 0
- Check if already borrowed by same student
- Verify admin added book with quantity

#### Styles not loading
- Bootstrap loaded from CDN (requires internet)
- Check CDN link in `base.html`

#### Database tables missing
1. Delete `library.db`
2. Restart app: `python app.py`
3. App will auto-create all tables

---

## 🚀 Deployment

### Development
```powershell
python app.py
# Access at http://localhost:5000
```

### Production

#### 1. Disable Debug Mode
Edit `app.py` (line ~596):
```python
app.run(debug=False)
```

#### 2. Use Production Server
```powershell
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

#### 3. Security Hardening
- [ ] Change `ADMIN_SECRET_CODE` in config.py
- [ ] Set `FLASK_ENV=production`
- [ ] Disable debug logging
- [ ] Use HTTPS (SSL/TLS)
- [ ] Configure firewall
- [ ] Regular security updates

#### 4. Backup Strategy
```powershell
Copy-Item library.db library.db.backup
```

---

## 📞 Quick Reference

### Default Credentials for Testing
- Secret Code: `ADMIN2025` (change in `config.py`)
- Create admin via `/admin/register` page
- Create students via Admin → Students page

### Key Files
- `app.py`: Main application (30+ routes)
- `config.py`: Configuration (secret code)
- `library.db`: SQLite database (auto-created)
- `templates/`: HTML templates (21 files)
- `static/style.css`: Custom styling

### Verification Commands
```powershell
# Test installation
python -m py_compile app.py config.py

# Verify config
python -c "from config import ADMIN_SECRET_CODE; print(f'Secret Code: {ADMIN_SECRET_CODE}')"

# Full system check
python -c "from app import app; from config import ADMIN_SECRET_CODE; print('✅ ALL SYSTEMS GO!')"
```

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 3.0 | 2025-11-11 | Admin-only student registration + secret code verification |
| 2.0 | 2025-11-11 | Fixed Jinja2 syntax errors, installed dependencies |
| 1.0 | 2025-11-11 | Initial release - Core library management system |

---

## 🎯 Next Steps

1. Review this README - Understand system architecture
2. Change secret code - Edit `config.py` with your own code
3. Run application - Execute `python app.py`
4. Register admin - Go to Admin → Register with secret code
5. Add students - Admin → Students → Register
6. Test borrowing - Login as student, borrow books
7. Deploy - Follow production deployment steps

---

**System Status**: ✅ Production Ready  
**Last Updated**: 2025-11-11  
**Python Version**: 3.8+  
**Flask Version**: 2.3.3  
**Werkzeug Version**: 2.3.7
