# Quick Start Guide - Library Management System

## Setup Instructions for Windows

### Step 1: Install Python (if not already installed)
1. Download Python from https://www.python.org/downloads/
2. Run the installer and check "Add Python to PATH"
3. Verify installation by opening PowerShell and typing:
   ```
   python --version
   ```

### Step 2: Navigate to Project Directory
Open PowerShell and run:
```powershell
cd "c:\Users\sahoo\Desktop\menagement\library_management"
```

### Step 3: Create Virtual Environment (Recommended)
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Run the Application
```powershell
python app.py
```

You should see:
```
WARNING: This is a development server. Do not use it in production deployments.
Running on http://127.0.0.1:5000
```

### Step 6: Access the Application
Open your web browser and go to:
```
http://localhost:5000
```

## Default Test Accounts

### Admin Account (Create First)
1. Click "Admin Login" → "Register here"
2. Create an account with:
   - Username: `admin`
   - Email: `admin@library.com`
   - Name: `Library Admin`
   - Password: `admin123`

### Student Account (Create Second)
1. Click "Student Login" → "Register here"
2. Create an account with:
   - Name: `John Doe`
   - Email: `john@student.com`
   - Roll Number: `2024001`
   - Department: `Computer Science`
   - Phone: `9876543210`
   - Password: `student123`

## Testing the System

### As Admin:
1. Login with admin credentials
2. Go to "Books" → "Add New Book"
3. Add some sample books
4. View dashboard statistics

### As Student:
1. Login with student credentials
2. Go to "Books" and borrow a book
3. View borrowed books in dashboard
4. Create a report for any issue
5. Return a book

## File Structure

```
library_management/
├── app.py                    # Main application (run this file)
├── library.db                # Database (created automatically)
├── requirements.txt          # Python packages
├── README.md                 # Full documentation
├── SETUP.md                  # This file
├── templates/                # HTML pages
│   ├── base.html
│   ├── index.html
│   ├── admin_*.html
│   ├── student_*.html
│   └── ...
└── static/
    └── css/
        └── style.css
```

## Common Commands

### Stop the Server
Press `Ctrl + C` in the PowerShell window

### Deactivate Virtual Environment
```powershell
deactivate
```

### Reset Database
Delete `library.db` file and restart the app

### Clear Python Cache
```powershell
Get-ChildItem -Path . -Filter "*.pyc" -Recurse | Remove-Item
Get-ChildItem -Path . -Filter "__pycache__" -Recurse | Remove-Item -Recurse
```

## Features Summary

✅ Student Registration & Login
✅ Admin Registration & Login
✅ Browse Book Catalog
✅ Borrow & Return Books
✅ Book Management (Add/Edit/Delete)
✅ Report Issues
✅ Admin Reports Management
✅ Database with SQLite
✅ Responsive Design
✅ Secure Authentication

## Troubleshooting

### "Module not found" Error
```powershell
pip install -r requirements.txt
```

### Port 5000 Already in Use
Edit app.py, change the port:
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Locked Error
Delete `library.db` and restart the application

### CSS Not Loading
Clear browser cache (Ctrl + Shift + Delete) and refresh

## System Requirements

- Windows 7 or higher
- Python 3.7+
- 100 MB free disk space
- Modern web browser (Chrome, Firefox, Edge)

## Need Help?

1. Check the README.md file for detailed documentation
2. Review the app.py comments for code explanation
3. Check browser console for JavaScript errors (F12)
4. Ensure all files are in correct directories

Enjoy using the Library Management System! 📚
