from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
from functools import wraps
from config import ADMIN_SECRET_CODE

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_this'
DATABASE = 'library.db'

# Database initialization
def init_db():
    """Initialize the database with tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Students table (add student_number for visible, sequential numbering)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_number INTEGER UNIQUE,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            roll_number TEXT UNIQUE NOT NULL,
            phone TEXT,
            department TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Admin table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (added_by) REFERENCES admin(id)
        )
    ''')
    
    # Book Issues (student borrowing books)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book_issues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            return_date TIMESTAMP,
            status TEXT DEFAULT 'borrowed',
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        )
    ''')
    
    # Reports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP,
            response TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    ''')

    # Admin actions / audit log
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS admin_actions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            admin_id INTEGER,
            action TEXT NOT NULL,
            target_type TEXT,
            target_id INTEGER,
            details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES admin(id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    """Decorator for routes that require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator for routes that require admin login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin login required', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== HOME & INDEX ====================
@app.route('/')
def index():
    """Home page"""
    return render_template('index.html')

# ==================== STUDENT ROUTES ====================
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    """Student login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM students WHERE email = ?', (email,))
        student = cursor.fetchone()
        conn.close()
        
        if student and check_password_hash(student['password'], password):
            session['user_id'] = student['id']
            session['user_name'] = student['name']
            session['user_type'] = 'student'
            flash(f'Welcome {student["name"]}!', 'success')
            return redirect(url_for('student_dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('student_login.html')

@app.route('/student/dashboard')
@login_required
def student_dashboard():
    """Student dashboard"""
    if session.get('user_type') != 'student':
        return redirect(url_for('student_login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get borrowed books
    cursor.execute('''
        SELECT bi.*, b.title, b.author, b.isbn
        FROM book_issues bi
        JOIN books b ON bi.book_id = b.id
        WHERE bi.student_id = ?
        ORDER BY bi.issue_date DESC
    ''', (session['user_id'],))
    borrowed_books = cursor.fetchall()
    
    conn.close()
    return render_template('student_dashboard.html', borrowed_books=borrowed_books)

@app.route('/student/books')
@login_required
def student_books():
    """View all available books"""
    if session.get('user_type') != 'student':
        return redirect(url_for('student_login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE available_quantity > 0')
    books = cursor.fetchall()
    conn.close()
    
    return render_template('student_books.html', books=books)

@app.route('/student/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    """Borrow a book"""
    if session.get('user_type') != 'student':
        return redirect(url_for('student_login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if book is available
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    
    if not book or book['available_quantity'] <= 0:
        flash('Book not available', 'danger')
        return redirect(url_for('student_books'))
    
    # Check if student already borrowed this book
    cursor.execute('''
        SELECT * FROM book_issues 
        WHERE student_id = ? AND book_id = ? AND status = 'borrowed'
    ''', (session['user_id'], book_id))
    
    if cursor.fetchone():
        flash('You already have this book', 'warning')
        return redirect(url_for('student_books'))
    
    # Issue the book
    cursor.execute('''
        INSERT INTO book_issues (student_id, book_id, status)
        VALUES (?, ?, 'borrowed')
    ''', (session['user_id'], book_id))
    
    # Update available quantity
    cursor.execute('''
        UPDATE books SET available_quantity = available_quantity - 1 WHERE id = ?
    ''', (book_id,))
    
    conn.commit()
    conn.close()
    
    flash('Book borrowed successfully!', 'success')
    return redirect(url_for('student_dashboard'))

@app.route('/student/return/<int:issue_id>', methods=['POST'])
@login_required
def return_book(issue_id):
    """Return a borrowed book"""
    if session.get('user_type') != 'student':
        return redirect(url_for('student_login'))
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM book_issues WHERE id = ?', (issue_id,))
    issue = cursor.fetchone()
    
    if not issue or issue['student_id'] != session['user_id']:
        flash('Invalid request', 'danger')
        return redirect(url_for('student_dashboard'))
    
    # Update issue status
    cursor.execute('''
        UPDATE book_issues SET status = 'returned', return_date = CURRENT_TIMESTAMP WHERE id = ?
    ''', (issue_id,))
    
    # Update available quantity
    cursor.execute('''
        UPDATE books SET available_quantity = available_quantity + 1 WHERE id = ?
    ''', (issue['book_id'],))
    
    conn.commit()
    conn.close()
    
    flash('Book returned successfully!', 'success')
    return redirect(url_for('student_dashboard'))

# ==================== ADMIN ROUTES ====================
@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    """Admin registration with verification code"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        secret_code = request.form.get('secret_code')
        
        # Verify secret code
        if secret_code != ADMIN_SECRET_CODE:
            flash('Invalid admin verification code!', 'danger')
            return redirect(url_for('admin_register'))
        
        if not all([username, email, name, password]):
            flash('All fields are required', 'danger')
            return redirect(url_for('admin_register'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            hashed_password = generate_password_hash(password)
            cursor.execute('''
                INSERT INTO admin (username, email, name, password)
                VALUES (?, ?, ?, ?)
            ''', (username, email, name, hashed_password))
            conn.commit()
            flash('Admin registration successful! Please login.', 'success')
            return redirect(url_for('admin_login'))
        except sqlite3.IntegrityError:
            flash('Username or Email already exists', 'danger')
        finally:
            conn.close()
    
    return render_template('admin_register.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = ?', (username,))
        admin = cursor.fetchone()
        conn.close()
        
        if admin and check_password_hash(admin['password'], password):
            session['admin_id'] = admin['id']
            session['admin_name'] = admin['name']
            session['user_type'] = 'admin'
            flash(f'Welcome Admin {admin["name"]}!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get statistics
    cursor.execute('SELECT COUNT(*) as count FROM students')
    total_students = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM books')
    total_books = cursor.fetchone()['count']
    
    cursor.execute('''
        SELECT COUNT(*) as count FROM book_issues WHERE status = 'borrowed'
    ''')
    books_borrowed = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM reports WHERE status = "open"')
    open_reports = cursor.fetchone()['count']
    
    conn.close()
    
    return render_template('admin_dashboard.html', 
                         total_students=total_students,
                         total_books=total_books,
                         books_borrowed=books_borrowed,
                         open_reports=open_reports)

@app.route('/admin/students', methods=['GET', 'POST'])
@admin_required
def admin_students():
    """Admin manage students - view and register new students"""
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'register':
            name = request.form.get('name')
            email = request.form.get('email')
            roll_number = request.form.get('roll_number')
            password = request.form.get('password')
            phone = request.form.get('phone')
            department = request.form.get('department')
            
            if not all([name, email, roll_number, password]):
                flash('All required fields must be filled', 'danger')
                return redirect(url_for('admin_students'))
            
            conn = get_db()
            cursor = conn.cursor()
            
            try:
                hashed_password = generate_password_hash(password)
                cursor.execute('''
                    INSERT INTO students (name, email, roll_number, password, phone, department)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (name, email, roll_number, hashed_password, phone, department))
                conn.commit()
                flash(f'Student {name} registered successfully!', 'success')
            except sqlite3.IntegrityError:
                flash('Email or Roll Number already exists', 'danger')
            finally:
                conn.close()
            
            return redirect(url_for('admin_students'))
        
        elif action == 'reset_password':
            student_id = request.form.get('student_id')
            new_password = request.form.get('new_password')
            if not student_id or not new_password:
                flash('Student ID and new password are required', 'danger')
                return redirect(url_for('admin_students'))

            conn = get_db()
            cursor = conn.cursor()
            hashed_password = generate_password_hash(new_password)
            cursor.execute('UPDATE students SET password = ? WHERE id = ?', (hashed_password, student_id))
            conn.commit()
            # Audit log: record who reset the student's password
            try:
                admin_id = session.get('admin_id')
                cursor.execute('''
                    INSERT INTO admin_actions (admin_id, action, target_type, target_id, details)
                    VALUES (?, ?, ?, ?, ?)
                ''', (admin_id, 'reset_student_password', 'student', student_id, f'Reset password for student_id={student_id}'))
                conn.commit()
            except Exception:
                # non-fatal if auditing fails
                pass
            # retrieve student name to display the freshly set plaintext to the admin
            try:
                cursor.execute('SELECT name FROM students WHERE id = ?', (student_id,))
                row = cursor.fetchone()
                student_name = row['name'] if row else ''
            except Exception:
                student_name = ''

            # Save the plaintext temporarily in session so it can be shown once after redirect
            session['last_reset'] = {
                'student_id': student_id,
                'password': new_password,
                'student_name': student_name,
            }

            conn.close()
            flash('Student password updated successfully!', 'success')
            return redirect(url_for('admin_students'))

        elif action == 'delete':
            student_id = request.form.get('student_id')
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            conn.commit()
            conn.close()
            flash('Student deleted successfully!', 'success')
            return redirect(url_for('admin_students'))
    
    # Get all students
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY created_at DESC')
    students = cursor.fetchall()
    conn.close()
    # If admin just reset a password, move that info into context and clear it from session
    last_reset = session.pop('last_reset', None)
    return render_template('admin_students.html', students=students, last_reset=last_reset)

@app.route('/admin/books')
@admin_required
def admin_books():
    """View all books (admin)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books ORDER BY created_at DESC')
    books = cursor.fetchall()
    conn.close()
    
    return render_template('admin_books.html', books=books)


@app.route('/admin/delete_account', methods=['POST'])
@admin_required
def delete_admin_account():
    """Allow admin to delete their own account after verifying secret code"""
    secret_code = request.form.get('secret_code')
    if secret_code != ADMIN_SECRET_CODE:
        flash('Invalid secret code!', 'danger')
        return redirect(url_for('admin_dashboard'))

    admin_id = session.get('admin_id')
    conn = get_db()
    cursor = conn.cursor()
    # Audit: record admin deletion
    try:
        cursor.execute('''
            INSERT INTO admin_actions (admin_id, action, target_type, target_id, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (admin_id, 'delete_admin_account', 'admin', admin_id, f'Admin id {admin_id} deleted their own account'))
        conn.commit()
    except Exception:
        pass

    cursor.execute('DELETE FROM admin WHERE id = ?', (admin_id,))
    conn.commit()
    conn.close()

    session.clear()
    flash('Your admin account has been deleted.', 'success')
    return redirect(url_for('index'))

@app.route('/admin/book/add', methods=['GET', 'POST'])
@admin_required
def add_book():
    """Add a new book"""
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        isbn = request.form.get('isbn')
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        published_year = request.form.get('published_year')
        image_url = request.form.get('image_url')
        
        if not all([title, author, isbn, category, quantity]):
            flash('All required fields must be filled', 'danger')
            return redirect(url_for('add_book'))
        
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO books (title, author, isbn, category, quantity, available_quantity, 
                                  description, published_year, image_url, added_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (title, author, isbn, category, int(quantity), int(quantity), 
                  description, published_year, image_url, session['admin_id']))
            conn.commit()
            flash('Book added successfully!', 'success')
            return redirect(url_for('admin_books'))
        except sqlite3.IntegrityError:
            flash('ISBN already exists', 'danger')
        finally:
            conn.close()
    
    return render_template('add_book.html')

@app.route('/admin/book/edit/<int:book_id>', methods=['GET', 'POST'])
@admin_required
def edit_book(book_id):
    """Edit a book"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        category = request.form.get('category')
        quantity = request.form.get('quantity')
        description = request.form.get('description')
        published_year = request.form.get('published_year')
        image_url = request.form.get('image_url')
        
        cursor.execute('''
            UPDATE books SET title = ?, author = ?, category = ?, quantity = ?, 
                           description = ?, published_year = ?, image_url = ?
            WHERE id = ?
        ''', (title, author, category, int(quantity), description, published_year, image_url, book_id))
        
        conn.commit()
        flash('Book updated successfully!', 'success')
        conn.close()
        return redirect(url_for('admin_books'))
    
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    
    if not book:
        flash('Book not found', 'danger')
        return redirect(url_for('admin_books'))
    
    return render_template('edit_book.html', book=book)

@app.route('/admin/book/delete/<int:book_id>', methods=['POST'])
@admin_required
def delete_book(book_id):
    """Delete a book"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('admin_books'))

# ==================== REPORTS ROUTES ====================
@app.route('/student/reports')
@login_required
def view_reports():
    """View reports (student)"""
    if session.get('user_type') != 'student':
        return redirect(url_for('student_login'))
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM reports WHERE student_id = ? ORDER BY created_at DESC
    ''', (session['user_id'],))
    reports = cursor.fetchall()
    conn.close()
    
    return render_template('student_reports.html', reports=reports)

@app.route('/student/report/create', methods=['GET', 'POST'])
@login_required
def create_report():
    """Create a library report"""
    if session.get('user_type') != 'student':
        return redirect(url_for('student_login'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        
        if not all([title, description, category]):
            flash('All fields are required', 'danger')
            return redirect(url_for('create_report'))
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reports (student_id, title, description, category, status)
            VALUES (?, ?, ?, ?, 'open')
        ''', (session['user_id'], title, description, category))
        conn.commit()
        conn.close()
        
        flash('Report submitted successfully!', 'success')
        return redirect(url_for('view_reports'))
    
    return render_template('create_report.html')

@app.route('/admin/reports')
@admin_required
def admin_reports():
    """View all reports (admin)"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT r.*, s.name as student_name, s.email
        FROM reports r
        LEFT JOIN students s ON r.student_id = s.id
        ORDER BY r.created_at DESC
    ''')
    reports = cursor.fetchall()
    conn.close()
    
    return render_template('admin_reports.html', reports=reports)

@app.route('/admin/report/<int:report_id>/respond', methods=['GET', 'POST'])
@admin_required
def respond_report(report_id):
    """Respond to a report"""
    conn = get_db()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        response = request.form.get('response')
        status = request.form.get('status')
        
        cursor.execute('''
            UPDATE reports SET response = ?, status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (response, status, report_id))
        
        conn.commit()
        flash('Report updated successfully!', 'success')
        conn.close()
        return redirect(url_for('admin_reports'))
    
    cursor.execute('''
        SELECT r.*, s.name as student_name, s.email
        FROM reports r
        LEFT JOIN students s ON r.student_id = s.id
        WHERE r.id = ?
    ''', (report_id,))
    report = cursor.fetchone()
    conn.close()
    
    if not report:
        flash('Report not found', 'danger')
        return redirect(url_for('admin_reports'))
    
    return render_template('respond_report.html', report=report)


@app.route('/admin/audit')
@admin_required
def admin_audit():
    """View admin action audit logs"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT aa.*, a.username as admin_username
        FROM admin_actions aa
        LEFT JOIN admin a ON aa.admin_id = a.id
        ORDER BY aa.created_at DESC
    ''')
    logs = cursor.fetchall()
    conn.close()
    return render_template('admin_audit.html', logs=logs)

@app.route('/admin/book_borrowing_history')
@admin_required
def admin_book_borrowing_history():
    """View all book borrowing history with student and book details"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Get all book issues with student and book details
    cursor.execute('''
        SELECT 
            bi.id,
            bi.issue_date,
            bi.return_date,
            bi.status,
            s.name as student_name,
            s.email as student_email,
            s.roll_number,
            b.title as book_title,
            b.author,
            b.isbn
        FROM book_issues bi
        JOIN students s ON bi.student_id = s.id
        JOIN books b ON bi.book_id = b.id
        ORDER BY bi.issue_date DESC
    ''')
    borrowing_history = cursor.fetchall()
    conn.close()
    
    return render_template('admin_book_borrowing.html', borrowing_history=borrowing_history)


@app.route('/admin/log_action', methods=['POST'])
@admin_required
def admin_log_action():
    """Endpoint to record admin UI actions (reveal/copy) into admin_actions"""
    data = request.get_json() or {}
    action = data.get('action')
    target_type = data.get('target_type')
    target_id = data.get('target_id')
    details = data.get('details')
    admin_id = session.get('admin_id')

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO admin_actions (admin_id, action, target_type, target_id, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (admin_id, action, target_type, target_id, details))
        conn.commit()
    except Exception:
        # Do not break UI if logging fails
        pass
    finally:
        try:
            conn.close()
        except Exception:
            pass

    return jsonify({'status': 'ok'})


@app.route('/admin/verify_action', methods=['POST'])
@admin_required
def admin_verify_action():
    """Verify admin password before allowing sensitive UI actions (reveal/copy).
    Expects JSON: { password, action, target_type, target_id, details }
    On success, inserts an admin_actions row noting the authorization and returns ok.
    """
    data = request.get_json() or {}
    password = data.get('password')
    action = data.get('action')
    target_type = data.get('target_type')
    target_id = data.get('target_id')
    details = data.get('details')

    admin_id = session.get('admin_id')
    if not admin_id or not password:
        return jsonify({'status': 'fail', 'message': 'Missing credentials'}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admin WHERE id = ?', (admin_id,))
    admin = cursor.fetchone()

    if not admin or not check_password_hash(admin['password'], password):
        conn.close()
        return jsonify({'status': 'fail', 'message': 'Invalid admin password'}), 403

    # record that admin authorized this action
    try:
        cursor.execute('''
            INSERT INTO admin_actions (admin_id, action, target_type, target_id, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (admin_id, f'authorize_{action}', target_type, target_id, details))
        conn.commit()
    except Exception:
        # non-fatal
        pass
    finally:
        conn.close()

    return jsonify({'status': 'ok'})

# ==================== LOGOUT ====================
@app.route('/logout')
def logout():
    """Logout"""
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

# ==================== RUN APP ====================
if __name__ == '__main__':
    # Always run init_db on startup to ensure any new tables (migrations)
    # are created. `CREATE TABLE IF NOT EXISTS` is idempotent so this is safe.
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
