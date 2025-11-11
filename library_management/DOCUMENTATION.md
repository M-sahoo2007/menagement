# College Library Management System - Complete Documentation

## 📚 Project Overview

A full-featured college library management system built with Python Flask and HTML/CSS/Bootstrap that enables students to borrow books and report issues, while administrators manage the library inventory and handle reports.

## 🎯 Key Features

### Student Portal
- ✅ User Registration with email, roll number, phone, and department
- ✅ Secure Login/Logout
- ✅ Browse Complete Book Catalog
- ✅ Borrow Available Books
- ✅ Return Borrowed Books
- ✅ View Borrow History
- ✅ Submit Library Issues/Reports
- ✅ Track Report Status and Responses
- ✅ Responsive Dashboard

### Admin Portal
- ✅ Admin Registration and Login
- ✅ Add New Books to Library
- ✅ Edit Book Information
- ✅ Delete Books from Library
- ✅ View Complete Book Inventory
- ✅ Track Book Availability
- ✅ View All Student Reports
- ✅ Respond to Student Reports
- ✅ Update Report Status
- ✅ Dashboard with Statistics

### Database Features
- ✅ SQLite Database (Auto-created)
- ✅ Secure Password Hashing
- ✅ Student Profiles
- ✅ Admin Profiles
- ✅ Book Inventory
- ✅ Book Issue Tracking
- ✅ Report Management
- ✅ Transaction History

## 📁 Project Directory Structure

```
c:\Users\sahoo\Desktop\menagement\library_management\
├── app.py                              # Main Flask application
├── library.db                          # SQLite database (auto-created)
├── requirements.txt                    # Python dependencies
├── README.md                           # Full documentation
├── SETUP.md                            # Setup instructions
├── templates/                          # HTML Templates
│   ├── base.html                       # Base template with navbar
│   ├── index.html                      # Home page
│   ├── student_register.html           # Student registration
│   ├── student_login.html              # Student login
│   ├── student_dashboard.html          # Student dashboard
│   ├── student_books.html              # Book browse page
│   ├── student_reports.html            # Student reports view
│   ├── create_report.html              # Create new report
│   ├── admin_register.html             # Admin registration
│   ├── admin_login.html                # Admin login
│   ├── admin_dashboard.html            # Admin dashboard
│   ├── admin_books.html                # Admin book list
│   ├── add_book.html                   # Add new book form
│   ├── edit_book.html                  # Edit book form
│   ├── admin_reports.html              # Admin reports view
│   ├── respond_report.html             # Respond to report form
│   ├── 404.html                        # Error page
│   └── 500.html                        # Server error page
└── static/                             # Static files
    └── css/
        └── style.css                   # Custom CSS styling

```

## 🛠️ Technologies Used

| Component | Technology |
|-----------|-----------|
| Backend Framework | Flask 2.3.3 |
| Database | SQLite3 |
| Security | Werkzeug (Password Hashing) |
| Frontend | HTML5, CSS3 |
| UI Framework | Bootstrap 5 |
| Icons | Font Awesome 6 |
| Sessions | Flask Session Management |

## 📊 Database Schema

### Students Table
```sql
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    roll_number TEXT UNIQUE NOT NULL,
    phone TEXT,
    department TEXT,
    created_at TIMESTAMP
)
```

### Admin Table
```sql
CREATE TABLE admin (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP
)
```

### Books Table
```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    isbn TEXT UNIQUE NOT NULL,
    category TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    available_quantity INTEGER NOT NULL,
    description TEXT,
    published_year INTEGER,
    image_url TEXT,
    added_by INTEGER,
    created_at TIMESTAMP,
    FOREIGN KEY (added_by) REFERENCES admin(id)
)
```

### Book Issues Table
```sql
CREATE TABLE book_issues (
    id INTEGER PRIMARY KEY,
    student_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL,
    issue_date TIMESTAMP,
    return_date TIMESTAMP,
    status TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
)
```

### Reports Table
```sql
CREATE TABLE reports (
    id INTEGER PRIMARY KEY,
    student_id INTEGER,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    response TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id)
)
```

## 🚀 Installation & Setup

### Prerequisites
- Windows 7 or higher
- Python 3.7 or higher
- pip (comes with Python)

### Installation Steps

1. **Open PowerShell** and navigate to project directory:
   ```powershell
   cd "c:\Users\sahoo\Desktop\menagement\library_management"
   ```

2. **Create Virtual Environment** (optional but recommended):
   ```powershell
   python -m venv venv
   venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run Application**:
   ```powershell
   python app.py
   ```

5. **Open Browser** and visit:
   ```
   http://localhost:5000
   ```

## 📖 Usage Guide

### For Students

**Registration:**
1. Click "Student Login" on home page
2. Click "Register here" link
3. Fill in all details:
   - Full Name
   - Email
   - Roll Number
   - Department
   - Phone Number
   - Password
4. Click "Register" button

**Login:**
1. Go to Student Login page
2. Enter email and password
3. Click Login

**Borrowing Books:**
1. Click "Books" in navigation
2. Browse available books
3. Click "Borrow Book" button
4. Book will appear in Dashboard

**Returning Books:**
1. Go to Dashboard
2. Find book in "My Borrowed Books"
3. Click "Return" button
4. Book returns to library

**Submitting Reports:**
1. Click "Reports" in navigation
2. Click "Create New Report"
3. Fill details:
   - Issue Title
   - Category (Book Issue, Damaged Book, Missing Book, etc.)
   - Detailed Description
4. Click "Submit Report"
5. Admin will respond within 24-48 hours

### For Admins

**Registration:**
1. Click "Admin Login" on home page
2. Click "Register here" link
3. Fill in:
   - Name
   - Username
   - Email
   - Password
4. Click Register

**Login:**
1. Go to Admin Login page
2. Enter username and password
3. Click Login

**Adding Books:**
1. Click "Books" in navigation
2. Click "Add New Book" button
3. Fill form:
   - Title
   - Author
   - ISBN (unique)
   - Category
   - Quantity
   - Published Year
   - Description
   - Image URL
4. Click "Add Book"

**Editing Books:**
1. Go to Books page
2. Find book and click "Edit"
3. Modify details (ISBN cannot be changed)
4. Click "Update Book"

**Managing Reports:**
1. Click "Reports" in navigation
2. View all student reports
3. Click "Respond" button
4. Write response and select status:
   - Open (not yet addressed)
   - In Progress (being worked on)
   - Resolved (completed)
5. Click "Submit Response"

**Dashboard:**
View statistics:
- Total Students
- Total Books
- Books Currently Borrowed
- Open Reports

## 🔐 Security Features

- ✅ Password Hashing using Werkzeug
- ✅ Session-based Authentication
- ✅ Login Required Decorators
- ✅ Role-based Access Control
- ✅ SQLite with proper data types
- ✅ Email and Username Uniqueness Validation

## 🎨 UI/UX Features

- ✅ Responsive Bootstrap 5 Design
- ✅ Mobile-friendly Layout
- ✅ Gradient Color Schemes
- ✅ Smooth Animations & Transitions
- ✅ Font Awesome Icons
- ✅ Clear Navigation
- ✅ Flash Messages for User Feedback
- ✅ Form Validation
- ✅ Hover Effects on Cards

## 📋 API Routes

### Student Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/student/register` | GET, POST | Student registration |
| `/student/login` | GET, POST | Student login |
| `/student/dashboard` | GET | Student dashboard |
| `/student/books` | GET | Browse books |
| `/student/borrow/<id>` | POST | Borrow a book |
| `/student/return/<id>` | POST | Return a book |
| `/student/reports` | GET | View student reports |
| `/student/report/create` | GET, POST | Create report |

### Admin Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/admin/register` | GET, POST | Admin registration |
| `/admin/login` | GET, POST | Admin login |
| `/admin/dashboard` | GET | Admin dashboard |
| `/admin/books` | GET | View all books |
| `/admin/book/add` | GET, POST | Add new book |
| `/admin/book/edit/<id>` | GET, POST | Edit book |
| `/admin/book/delete/<id>` | POST | Delete book |
| `/admin/reports` | GET | View all reports |
| `/admin/report/<id>/respond` | GET, POST | Respond to report |

### General Routes
| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Home page |
| `/logout` | GET | Logout user |

## 🧪 Testing the System

### Create Sample Data as Admin:
1. Login as admin
2. Add 5-10 books with different categories
3. Add descriptions and images
4. View dashboard statistics

### Test as Student:
1. Create student account
2. Borrow 2-3 books
3. Return 1 book
4. Create a test report
5. Check report in dashboard

### Test Admin Features:
1. Verify books appear in admin list
2. Edit a book
3. Delete a book (if no issues)
4. Respond to student report
5. Check dashboard updates

## 🐛 Troubleshooting

### Issue: Module not found
**Solution:**
```powershell
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution:** Edit app.py line 283:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue: Database locked
**Solution:** Delete `library.db` and restart app

### Issue: CSS not loading
**Solution:** Clear browser cache (Ctrl+Shift+Delete) and refresh

### Issue: Login always fails
**Solution:** 
- Check email/username spelling
- Ensure database file exists
- Check browser console for errors

## 📈 Future Enhancement Ideas

- Email notifications for report updates
- Book reservation system
- Fine management for overdue books
- Advanced search with filters
- Book ratings and reviews
- User dashboard analytics
- PDF report generation
- SMS notifications
- Barcode/QR code system
- Mobile app version
- Payment gateway for fine payment
- Book recommendation system
- Integration with RFID tags

## 💾 Backup & Recovery

### Backup Database:
```powershell
Copy-Item library.db library.db.backup
```

### Restore Database:
```powershell
Copy-Item library.db.backup library.db
```

### Reset Database:
```powershell
Remove-Item library.db
```
(Restart app to recreate)

## 📞 Support

For issues or questions:
1. Check README.md for detailed documentation
2. Review SETUP.md for installation help
3. Check app.py for code comments
4. Review browser console (F12) for errors
5. Ensure all files are in correct directories

## 📜 License

This project is open source and available for educational purposes.

## 👨‍💻 Version Info

- **Version**: 1.0
- **Created**: 2025
- **Python**: 3.7+
- **Flask**: 2.3.3

---

**Happy Learning! 📚** 

The Library Management System is ready to use. Start by running `python app.py` and visiting `http://localhost:5000`
