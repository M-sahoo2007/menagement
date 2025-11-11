# 🗺️ COMPLETE API ROUTES & ENDPOINTS

## 📍 All Routes in Library Management System

---

## 🏠 PUBLIC ROUTES (No Login Required)

### Home Page
```
GET /
File: templates/index.html
Shows: Home page with features and login options
```

### Student Registration
```
GET  /student/register
POST /student/register
File: templates/student_register.html
Action: Register new student account
```

### Student Login
```
GET  /student/login
POST /student/login
File: templates/student_login.html
Action: Login with email and password
```

### Admin Registration
```
GET  /admin/register
POST /admin/register
File: templates/admin_register.html
Action: Register new admin account
```

### Admin Login
```
GET  /admin/login
POST /admin/login
File: templates/admin_login.html
Action: Login with username and password
```

### Logout
```
GET /logout
Action: Clear session and logout
Redirects to: Home page
```

### Error Pages
```
GET 404   - Page not found (invalid URL)
GET 500   - Server error
Files: templates/404.html, templates/500.html
```

---

## 👨‍🎓 STUDENT ROUTES (Login Required)

### Student Dashboard
```
GET /student/dashboard
File: templates/student_dashboard.html
Shows: 
  - Borrowed books
  - Return history
  - Quick access buttons
Requires: Student login
```

### Browse Books
```
GET /student/books
File: templates/student_books.html
Shows: All available books with grid layout
Requires: Student login
Displays: 
  - Book title, author, ISBN
  - Category, available quantity
  - Description, image
  - Borrow button (if available)
```

### Borrow Book
```
POST /student/borrow/<book_id>
Parameters: book_id (integer)
Action: Add book to student's borrowed list
Updates: Decreases available_quantity by 1
Requires: Student login, book available
Redirects: Back to dashboard
```

### Return Book
```
POST /student/return/<issue_id>
Parameters: issue_id (integer)
Action: Mark book as returned
Updates: Increases available_quantity by 1, sets status to 'returned'
Requires: Student login, active borrow record
Redirects: Back to dashboard
```

### View Reports
```
GET /student/reports
File: templates/student_reports.html
Shows: All reports submitted by student
Requires: Student login
Displays:
  - Report title, status, date
  - Admin response (if available)
  - Create new report button
```

### Create Report
```
GET  /student/report/create
POST /student/report/create
File: templates/create_report.html
Fields:
  - Title (text input)
  - Category (dropdown: Book Issue, Damaged Book, Missing Book, Facility Issue, Staff Issue, System Error, Other)
  - Description (textarea)
Action: Save new report to database
Requires: Student login
Redirects: To student reports page
```

---

## 👨‍💼 ADMIN ROUTES (Login Required)

### Admin Dashboard
```
GET /admin/dashboard
File: templates/admin_dashboard.html
Shows:
  - Total students count
  - Total books count
  - Books currently borrowed
  - Open reports count
  - Quick action buttons
Requires: Admin login
```

### View All Books
```
GET /admin/books
File: templates/admin_books.html
Shows: Complete book inventory table
Requires: Admin login
Displays:
  - Title, Author, ISBN
  - Category, Total quantity, Available quantity
  - Published year
  - Edit and Delete buttons for each book
```

### Add New Book
```
GET  /admin/book/add
POST /admin/book/add
File: templates/add_book.html
Fields:
  - Title (required)
  - Author (required)
  - ISBN (required, unique)
  - Category (required)
  - Quantity (required)
  - Published Year (optional)
  - Description (optional)
  - Image URL (optional)
Action: Save new book to database
Requires: Admin login
Validations:
  - ISBN must be unique
  - All required fields filled
Redirects: To admin books page
```

### Edit Book
```
GET  /admin/book/edit/<book_id>
POST /admin/book/edit/<book_id>
Parameters: book_id (integer)
File: templates/edit_book.html
Editable Fields:
  - Title
  - Author
  - Category
  - Quantity (total)
  - Published Year
  - Description
  - Image URL
Non-editable:
  - ISBN
  - Current stock information (display only)
Action: Update book information
Requires: Admin login, book exists
Redirects: To admin books page
```

### Delete Book
```
POST /admin/book/delete/<book_id>
Parameters: book_id (integer)
Action: Remove book from database
Requires: Admin login
Confirmation: User must confirm delete
Redirects: To admin books page
```

### View All Reports
```
GET /admin/reports
File: templates/admin_reports.html
Shows: All reports from all students
Requires: Admin login
Displays:
  - Report statistics (Total, Open, In Progress, Resolved)
  - Table with:
    - Report ID
    - Student name
    - Student email
    - Report title
    - Category
    - Date submitted
    - Status
    - Respond button
```

### Respond to Report
```
GET  /admin/report/<report_id>/respond
POST /admin/report/<report_id>/respond
Parameters: report_id (integer)
File: templates/respond_report.html
Shows:
  - Complete report details
  - Student information
  - Current status
Response Fields:
  - Status dropdown (Open, In Progress, Resolved)
  - Response textarea
Action: Save response and update report status
Requires: Admin login
Redirects: To admin reports page
```

---

## 🔐 AUTHENTICATION ROUTES

### Login Check
All student routes check:
```python
@login_required
if session.get('user_type') == 'student':
```

All admin routes check:
```python
@admin_required
if session.get('admin_id') not in session:
```

### Session Management
```
Session Variables:
- user_id (for students)
- user_name (for students)
- user_type (student/admin/none)
- admin_id (for admins)
- admin_name (for admins)
```

---

## 📊 COMPLETE ROUTE SUMMARY TABLE

| HTTP Method | Route | Purpose | Login Required | File |
|-------------|-------|---------|---|---|
| GET | `/` | Home page | No | index.html |
| GET, POST | `/student/register` | Student signup | No | student_register.html |
| GET, POST | `/student/login` | Student login | No | student_login.html |
| GET | `/student/dashboard` | Student dashboard | Yes (Student) | student_dashboard.html |
| GET | `/student/books` | Browse books | Yes (Student) | student_books.html |
| POST | `/student/borrow/<id>` | Borrow a book | Yes (Student) | - |
| POST | `/student/return/<id>` | Return a book | Yes (Student) | - |
| GET | `/student/reports` | View reports | Yes (Student) | student_reports.html |
| GET, POST | `/student/report/create` | Create report | Yes (Student) | create_report.html |
| GET, POST | `/admin/register` | Admin signup | No | admin_register.html |
| GET, POST | `/admin/login` | Admin login | No | admin_login.html |
| GET | `/admin/dashboard` | Admin dashboard | Yes (Admin) | admin_dashboard.html |
| GET | `/admin/books` | Manage books | Yes (Admin) | admin_books.html |
| GET, POST | `/admin/book/add` | Add book | Yes (Admin) | add_book.html |
| GET, POST | `/admin/book/edit/<id>` | Edit book | Yes (Admin) | edit_book.html |
| POST | `/admin/book/delete/<id>` | Delete book | Yes (Admin) | - |
| GET | `/admin/reports` | View all reports | Yes (Admin) | admin_reports.html |
| GET, POST | `/admin/report/<id>/respond` | Respond to report | Yes (Admin) | respond_report.html |
| GET | `/logout` | Logout | Any | - |

---

## 🔄 REQUEST/RESPONSE FLOW

### Student Registration Flow
```
POST /student/register
├─ Validate form data
├─ Hash password
├─ Check duplicate email/roll number
├─ Save to database
├─ Flash success message
└─ Redirect to /student/login
```

### Book Borrowing Flow
```
POST /student/borrow/<id>
├─ Check login status
├─ Get book details
├─ Check availability
├─ Check not already borrowed
├─ Create book_issue record
├─ Decrease available_quantity
├─ Commit to database
├─ Flash success message
└─ Redirect to /student/dashboard
```

### Report Submission Flow
```
POST /student/report/create
├─ Check login status
├─ Validate form fields
├─ Create report record
├─ Set status to 'open'
├─ Save to database
├─ Flash success message
└─ Redirect to /student/reports
```

### Admin Report Response Flow
```
POST /admin/report/<id>/respond
├─ Check admin login
├─ Get report details
├─ Update response field
├─ Update status
├─ Set updated_at timestamp
├─ Commit to database
├─ Flash success message
└─ Redirect to /admin/reports
```

---

## 📝 QUERY PARAMETERS

### Book Filtering
```
/student/books
Shows only books where available_quantity > 0
```

### Report Filtering
```
/student/reports
Shows only reports where student_id = current_user_id

/admin/reports
Shows all reports from all students
```

### Book Issues
```
/student/dashboard
Shows all book_issues for current student
Joins with books table to display details
```

---

## 🗄️ DATABASE RELATIONSHIPS

```
students (1) ──── (∞) book_issues (∞) ──── (1) books
   │                                           │
   │                                           └──── admin
   │
   └──────── (1) (∞) reports
```

---

## ✅ ROUTE VALIDATION

### Student Routes Validation:
- User must be logged in
- user_type must be 'student'
- user_id must exist in session

### Admin Routes Validation:
- User must be logged in
- user_type must be 'admin'
- admin_id must exist in session

### Public Routes:
- No login required
- Can be accessed by anyone

---

## 🔗 ROUTE REDIRECTION RULES

```
No Login → Protected Route
  └─ Redirect to appropriate login page
  
Wrong User Type → Protected Route
  └─ Redirect to appropriate login page

Post Action Success
  └─ Redirect to relevant list/dashboard

Post Action Error
  └─ Redirect to form (data preserved in errors)

Logout
  └─ Always redirect to home page
```

---

## 📊 DATA FLOW DIAGRAM

```
User Input
   │
   ├─ Form Data
   ├─ URL Parameters
   └─ Session Data
        │
        ▼
    Flask Route
        │
        ├─ Validation
        ├─ Authentication
        └─ Authorization
        │
        ▼
    Database Operation
        │
        ├─ Query
        ├─ Insert
        ├─ Update
        └─ Delete
        │
        ▼
    Response
        │
        ├─ Render Template
        ├─ Flash Message
        └─ Redirect
        │
        ▼
    User Interface
```

---

## 🎯 COMMON ENDPOINT PATTERNS

### Read Operations (GET)
- `/student/books` - Get all books
- `/student/dashboard` - Get student's data
- `/admin/books` - Get all books
- `/admin/reports` - Get all reports

### Write Operations (POST)
- `/student/register` - Create account
- `/student/borrow/<id>` - Create issue record
- `/admin/book/add` - Create book
- `/admin/report/<id>/respond` - Update report

### Update Operations (POST)
- `/admin/book/edit/<id>` - Update book
- `/admin/report/<id>/respond` - Update report

### Delete Operations (POST)
- `/admin/book/delete/<id>` - Delete book

---

**Total Routes: 25+**

**Public Routes: 6**

**Student Routes: 9**

**Admin Routes: 9**

**Authentication Routes: 1**

---

For implementation details, see `app.py`
For visual navigation, check templates in `templates/` folder
