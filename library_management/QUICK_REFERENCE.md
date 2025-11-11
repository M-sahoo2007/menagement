# Library Management System - Quick Reference

## 🚀 Quick Start (30 seconds)

```powershell
cd "c:\Users\sahoo\Desktop\menagement\library_management"
pip install -r requirements.txt
python app.py
```

Then visit: **http://localhost:5000**

---

## 📚 System Overview

```
LIBRARY MANAGEMENT SYSTEM
│
├─ STUDENT PORTAL
│  ├─ Register & Login
│  ├─ Browse Books
│  ├─ Borrow/Return Books
│  └─ Submit & Track Reports
│
└─ ADMIN PORTAL
   ├─ Register & Login
   ├─ Add/Edit/Delete Books
   ├─ Manage Book Inventory
   └─ Handle Student Reports
```

---

## 🔑 Key Login Credentials (After Setup)

### Create Admin First:
```
Username: admin
Password: admin123
```

### Create Student:
```
Email: student@college.com
Roll: 2024001
Password: student123
```

---

## 📂 Project Files

| File | Purpose |
|------|---------|
| `app.py` | Main application - RUN THIS |
| `library.db` | Database (auto-created) |
| `requirements.txt` | Python packages to install |
| `README.md` | Full documentation |
| `SETUP.md` | Installation guide |
| `DOCUMENTATION.md` | Complete guide |
| `templates/` | HTML pages (20 files) |
| `static/css/style.css` | Styling |

---

## 🎯 Main Features at a Glance

### Student Features:
- ✅ Register with email & roll number
- ✅ Login securely
- ✅ Browse book catalog
- ✅ Borrow available books
- ✅ Return books anytime
- ✅ View borrow history
- ✅ Report library issues
- ✅ Track report status

### Admin Features:
- ✅ Register & Login
- ✅ Add new books
- ✅ Edit book details
- ✅ Delete books
- ✅ View inventory
- ✅ Check statistics
- ✅ Respond to reports
- ✅ Update report status

---

## 🗄️ Database Tables

1. **Students** - Student profiles
2. **Admin** - Administrator accounts
3. **Books** - Book inventory
4. **Book Issues** - Borrow/return records
5. **Reports** - Student issue reports

---

## 🔧 Configuration

**Change Port (if 5000 is busy):**
Edit `app.py`, find line `app.run(...)` and change port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

**Change Secret Key (for production):**
Edit `app.py`, line:
```python
app.secret_key = 'your_secret_key_change_this'
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| Module not found | `pip install -r requirements.txt` |
| Port 5000 in use | Change port in app.py |
| Database locked | Delete library.db and restart |
| CSS not loading | Clear cache (Ctrl+Shift+Delete) |
| Forgot password | Delete library.db to reset all data |

---

## 📋 Student User Journey

1. **Home** → Click "Student Login"
2. **Register** → Fill form → Create account
3. **Login** → Email + Password → Dashboard
4. **Dashboard** → See options for Books/Reports
5. **Browse Books** → Click "Borrow Book"
6. **My Books** → Shows borrowed books
7. **Return** → Click "Return" to return book
8. **Reports** → "Create New Report" for issues
9. **Logout** → Click Logout

---

## 📋 Admin User Journey

1. **Home** → Click "Admin Login"
2. **Register** → Fill form → Create account
3. **Login** → Username + Password → Dashboard
4. **Dashboard** → See statistics
5. **Books** → Add/Edit/Delete books
6. **Add Book** → Fill details → Add to library
7. **Reports** → View student reports
8. **Respond** → Write response + Update status
9. **Logout** → Click Logout

---

## 📊 Report Categories

- Book Issue
- Damaged Book
- Missing Book
- Facility Issue
- Staff Issue
- System Error
- Other

---

## 🎨 Technology Stack

```
FRONTEND:
├─ HTML5
├─ CSS3
├─ Bootstrap 5
└─ Font Awesome Icons

BACKEND:
├─ Python 3.7+
├─ Flask 2.3.3
└─ Werkzeug (Security)

DATABASE:
└─ SQLite3

FEATURES:
├─ Session Management
├─ Password Hashing
├─ Form Validation
└─ Error Handling
```

---

## 📦 Dependencies

Only 2 packages needed:
```
Flask==2.3.3
Werkzeug==2.3.7
```

---

## 📞 File Locations

```
c:\Users\sahoo\Desktop\menagement\
└─ library_management\
   ├─ app.py
   ├─ library.db
   ├─ templates\ (20 HTML files)
   ├─ static\css\style.css
   └─ requirements.txt
```

---

## 🎓 Testing Checklist

- [ ] App starts without errors
- [ ] Can register student account
- [ ] Can register admin account
- [ ] Student can login
- [ ] Admin can login
- [ ] Can add book as admin
- [ ] Can borrow book as student
- [ ] Can return book as student
- [ ] Can create report as student
- [ ] Can respond to report as admin
- [ ] Dashboard shows correct stats
- [ ] Logout works properly

---

## 💾 Important Files to Keep Safe

- `library.db` - Your database with all data
- `app.py` - The application code
- `templates/` - All HTML pages

---

## 🔄 Common Tasks

### Create Backup:
```powershell
Copy-Item library.db library_backup.db
```

### Reset Everything:
```powershell
Remove-Item library.db
```

### Stop Server:
Press **Ctrl + C** in PowerShell

### View Database:
Download SQLite Browser to view library.db

---

## 🌐 Navigation URLs

| Page | URL | Access |
|------|-----|--------|
| Home | http://localhost:5000/ | Anyone |
| Student Register | http://localhost:5000/student/register | Anyone |
| Student Login | http://localhost:5000/student/login | Anyone |
| Admin Register | http://localhost:5000/admin/register | Anyone |
| Admin Login | http://localhost:5000/admin/login | Anyone |
| Student Dashboard | http://localhost:5000/student/dashboard | Students Only |
| Books | http://localhost:5000/student/books | Students Only |
| Reports | http://localhost:5000/student/reports | Students Only |
| Admin Dashboard | http://localhost:5000/admin/dashboard | Admins Only |
| Manage Books | http://localhost:5000/admin/books | Admins Only |
| All Reports | http://localhost:5000/admin/reports | Admins Only |

---

## 🚨 Important Notes

1. **First time**: Database auto-creates when app runs
2. **Passwords**: Never saved in plain text (hashed)
3. **Unique**: Email (student) and Username (admin) must be unique
4. **Sessions**: Automatically logged out if inactive
5. **Port**: Default 5000, can be changed if needed

---

## 📱 Responsive Design

- ✅ Works on Desktop
- ✅ Works on Tablet
- ✅ Works on Mobile
- ✅ Bootstrap 5 responsive grid
- ✅ Hamburger menu on small screens

---

**Created**: 2025 | **Version**: 1.0 | **Status**: Ready to Use ✅

For complete details, see: **README.md**, **SETUP.md**, or **DOCUMENTATION.md**
