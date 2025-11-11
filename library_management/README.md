# College Library Management System

A comprehensive web-based library management system built with Python (Flask) and HTML/CSS/Bootstrap. This system allows students to browse and borrow books, while administrators can manage the library inventory and handle student reports.

## Features

### Student Features
- **User Registration & Login**: Secure registration and authentication for students
- **Browse Books**: View all available books in the library catalog
- **Borrow Books**: Borrow books from the library
- **Return Books**: Return borrowed books to the library
- **Dashboard**: Track borrowed books and return history
- **Report Issues**: Submit reports for library-related problems
- **Track Reports**: View status and responses to submitted reports

### Admin Features
- **Admin Registration & Login**: Secure admin authentication
- **Book Management**: Add, edit, and delete books
- **Inventory Management**: Track book quantities and availability
- **Statistics Dashboard**: View library statistics (total students, books, borrowed books, open reports)
- **Book Catalog**: View and manage all books in the library
- **Report Management**: View and respond to student reports
- **Report Status Updates**: Update report status (open, in_progress, resolved)

### Database Features
- SQLite database for data persistence
- Secure password hashing with Werkzeug
- Relationship between students, books, and transactions
- Report tracking and responses

## Project Structure

```
library_management/
├── app.py                          # Main Flask application
├── library.db                      # SQLite database (auto-created)
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── templates/                      # HTML templates
│   ├── base.html                   # Base template with navigation
│   ├── index.html                  # Home page
│   ├── student_register.html       # Student registration
│   ├── student_login.html          # Student login
│   ├── student_dashboard.html      # Student dashboard
│   ├── student_books.html          # Browse books
│   ├── student_reports.html        # View reports
│   ├── create_report.html          # Create new report
│   ├── admin_register.html         # Admin registration
│   ├── admin_login.html            # Admin login
│   ├── admin_dashboard.html        # Admin dashboard
│   ├── admin_books.html            # Manage books
│   ├── add_book.html               # Add new book
│   ├── edit_book.html              # Edit book details
│   ├── admin_reports.html          # View all reports
│   ├── respond_report.html         # Respond to reports
│   ├── 404.html                    # Page not found
│   └── 500.html                    # Server error
└── static/                         # Static files
    └── css/
        └── style.css               # Custom CSS styles
```

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Steps to Install

1. **Navigate to project directory**:
   ```bash
   cd c:\Users\sahoo\Desktop\menagement\library_management
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Access the application**:
   - Open your browser and go to: `http://localhost:5000`

## Database Schema

### Students Table
- id (Primary Key)
- name
- email (Unique)
- password (hashed)
- roll_number (Unique)
- phone
- department
- created_at

### Admin Table
- id (Primary Key)
- username (Unique)
- email (Unique)
- password (hashed)
- name
- created_at

### Books Table
- id (Primary Key)
- title
- author
- isbn (Unique)
- category
- quantity
- available_quantity
- description
- published_year
- image_url
- added_by (Foreign Key - Admin)
- created_at

### Book Issues Table
- id (Primary Key)
- student_id (Foreign Key)
- book_id (Foreign Key)
- issue_date
- return_date
- status (borrowed/returned)

### Reports Table
- id (Primary Key)
- student_id (Foreign Key)
- title
- description
- category
- status (open/in_progress/resolved)
- created_at
- updated_at
- response

## User Workflows

### Student Workflow
1. Register as a student with email, roll number, and password
2. Login with email and password
3. Browse available books in the library
4. Borrow books (limited to available quantity)
5. View borrowed books in dashboard
6. Return borrowed books anytime
7. Submit reports for any library issues
8. Track report status and view admin responses

### Admin Workflow
1. Register as an admin with username and password
2. Login with username and password
3. View dashboard with library statistics
4. Add new books with all details
5. Edit existing book information
6. Delete books from the library
7. View all student reports
8. Respond to reports and update status
9. Track borrowed books and student activity

## Features in Detail

### Book Management
- Add books with title, author, ISBN, category, quantity, and description
- Edit book details (except ISBN)
- Delete books from the library
- Track available quantity automatically
- Support for book cover images

### Borrowing System
- Students can borrow books if available
- System prevents duplicate borrowing
- Track borrowed and returned books
- Automatic inventory update
- Return history for students

### Report System
- Students can report library issues
- Categories: Book Issue, Damaged Book, Missing Book, Facility Issue, Staff Issue, System Error, Other
- Admins can respond to reports
- Track report status (Open, In Progress, Resolved)
- Students can view admin responses

### Security
- Password hashing using Werkzeug
- Session-based authentication
- Login required decorators
- Role-based access control (Student/Admin)
- CSRF protection through Flask

## Technologies Used

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Icons**: Font Awesome
- **Security**: Werkzeug (Password Hashing)

## Configuration

### Change Secret Key
Edit the secret key in `app.py` for production:
```python
app.secret_key = 'your_secret_key_change_this'  # Change this!
```

### Database Location
The database is created automatically as `library.db` in the project root.

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, change it in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Reset
Delete `library.db` and restart the app to reset the database.

### Login Issues
- Ensure you're using the correct email (for students) or username (for admins)
- Passwords are case-sensitive

## Future Enhancements

- Email notifications for report updates
- Book reservation system
- Fine management for overdue books
- Advanced search and filtering
- Book rating and reviews
- User dashboard analytics
- PDF report generation
- SMS notifications
- Mobile app version

## License

This project is open source and available for educational purposes.

## Support

For any issues or questions, please contact the library administrator.

---

**Developed**: 2025
**Version**: 1.0
