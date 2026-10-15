import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, send_from_directory

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'web_templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'src', 'main', 'resources', 'static'),
    static_url_path='/static'
)
app.secret_key = 'apex-college-sms-secret-key-2024'

DB_PATH = os.path.join(os.path.dirname(__file__), 'student_db.sqlite')

SUBJECTS = [
    'Object Oriented Programming',
    'Database Management Systems',
    'Data Structures & Algorithms',
    'Computer Networks',
    'Operating Systems'
]

DEPARTMENTS = ['CSE', 'IT', 'AI&DS', 'ENTC', 'Mechanical', 'Civil']

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'ADMIN'
    );

    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        department TEXT NOT NULL,
        class_year TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        phone TEXT NOT NULL,
        address TEXT,
        dob TEXT NOT NULL,
        gender TEXT NOT NULL,
        admission_date TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS marks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject TEXT NOT NULL,
        marks_obtained REAL NOT NULL,
        max_marks REAL DEFAULT 100.0,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        total_classes INTEGER NOT NULL DEFAULT 0,
        attended_classes INTEGER NOT NULL DEFAULT 0,
        FOREIGN KEY (student_id) REFERENCES students(id) ON DELETE CASCADE
    );
    ''')
    conn.commit()

    # Seed initial data if students table is empty
    cursor.execute('SELECT COUNT(*) FROM students')
    if cursor.fetchone()[0] == 0:
        # 1. Users
        cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('admin', 'admin123', 'ADMIN')")
        cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES ('teacher', 'teacher123', 'TEACHER')")

        # 2. Students
        seed_students = [
            (1, 'STU2024001', 'Aarav Sharma', 'CSE', 'TE', 'aarav.sharma@college.edu', '9876543210', '124 MG Road, Pune, Maharashtra', '2003-05-14', 'Male', '2022-08-01'),
            (2, 'STU2024002', 'Priya Patel', 'IT', 'TE', 'priya.patel@college.edu', '9823456781', '45 Park Avenue, Mumbai, Maharashtra', '2003-08-22', 'Female', '2022-08-01'),
            (3, 'STU2024003', 'Rohan Verma', 'AI&DS', 'SE', 'rohan.verma@college.edu', '9812345678', '78 Shivaji Nagar, Pune, Maharashtra', '2004-02-10', 'Male', '2023-08-10'),
            (4, 'STU2024004', 'Ananya Deshmukh', 'ENTC', 'BE', 'ananya.d@college.edu', '9890123456', '12 Kothrud, Pune, Maharashtra', '2002-11-05', 'Female', '2021-08-15'),
            (5, 'STU2024005', 'Vikramaditya Singh', 'Mechanical', 'TE', 'vikram.singh@college.edu', '9765432109', '56 Model Colony, Pune, Maharashtra', '2003-07-19', 'Male', '2022-08-01'),
            (6, 'STU2024006', 'Sneha Kulkarni', 'CSE', 'FE', 'sneha.k@college.edu', '9845123478', '89 Baner Road, Pune, Maharashtra', '2005-03-30', 'Female', '2024-08-05'),
            (7, 'STU2024007', 'Aditi Rao', 'Civil', 'SE', 'aditi.rao@college.edu', '9734567890', '23 Koregaon Park, Pune, Maharashtra', '2004-09-12', 'Female', '2023-08-10'),
            (8, 'STU2024008', 'Rahul Joshi', 'IT', 'BE', 'rahul.joshi@college.edu', '9822334455', '67 Viman Nagar, Pune, Maharashtra', '2002-04-18', 'Male', '2021-08-15'),
            (9, 'STU2024009', 'Tanvi Shinde', 'AI&DS', 'FE', 'tanvi.s@college.edu', '9811223344', '34 Aundh, Pune, Maharashtra', '2005-01-25', 'Female', '2024-08-05'),
            (10, 'STU2024010', 'Siddharth Mehta', 'ENTC', 'TE', 'siddharth.m@college.edu', '9877889900', '101 FC Road, Pune, Maharashtra', '2003-12-08', 'Male', '2022-08-01'),
            (11, 'STU2024011', 'Neha Gupta', 'Mechanical', 'BE', 'neha.gupta@college.edu', '9866554433', '15 Deccan Gymkhana, Pune, Maharashtra', '2002-06-15', 'Female', '2021-08-15'),
            (12, 'STU2024012', 'Harsh Vardhan', 'Civil', 'FE', 'harsh.v@college.edu', '9855443322', '88 Hadapsar, Pune, Maharashtra', '2005-08-02', 'Male', '2024-08-05')
        ]
        cursor.executemany('''
            INSERT INTO students (id, student_id, name, department, class_year, email, phone, address, dob, gender, admission_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', seed_students)

        # 3. Marks (5 subjects each)
        seed_marks = [
            (1, 'Object Oriented Programming', 88.0), (1, 'Database Management Systems', 92.0), (1, 'Data Structures & Algorithms', 85.0), (1, 'Computer Networks', 78.0), (1, 'Operating Systems', 84.0),
            (2, 'Object Oriented Programming', 95.0), (2, 'Database Management Systems', 94.0), (2, 'Data Structures & Algorithms', 91.0), (2, 'Computer Networks', 89.0), (2, 'Operating Systems', 93.0),
            (3, 'Object Oriented Programming', 72.0), (3, 'Database Management Systems', 68.0), (3, 'Data Structures & Algorithms', 75.0), (3, 'Computer Networks', 64.0), (3, 'Operating Systems', 70.0),
            (4, 'Object Oriented Programming', 81.0), (4, 'Database Management Systems', 85.0), (4, 'Data Structures & Algorithms', 79.0), (4, 'Computer Networks', 88.0), (4, 'Operating Systems', 82.0),
            (5, 'Object Oriented Programming', 62.0), (5, 'Database Management Systems', 58.0), (5, 'Data Structures & Algorithms', 65.0), (5, 'Computer Networks', 55.0), (5, 'Operating Systems', 60.0),
            (6, 'Object Oriented Programming', 78.0), (6, 'Database Management Systems', 80.0), (6, 'Data Structures & Algorithms', 82.0), (6, 'Computer Networks', 74.0), (6, 'Operating Systems', 76.0),
            (7, 'Object Oriented Programming', 55.0), (7, 'Database Management Systems', 62.0), (7, 'Data Structures & Algorithms', 58.0), (7, 'Computer Networks', 50.0), (7, 'Operating Systems', 54.0),
            (8, 'Object Oriented Programming', 45.0), (8, 'Database Management Systems', 48.0), (8, 'Data Structures & Algorithms', 32.0), (8, 'Computer Networks', 40.0), (8, 'Operating Systems', 42.0),
            (9, 'Object Oriented Programming', 89.0), (9, 'Database Management Systems', 91.0), (9, 'Data Structures & Algorithms', 87.0), (9, 'Computer Networks', 85.0), (9, 'Operating Systems', 90.0),
            (10, 'Object Oriented Programming', 74.0), (10, 'Database Management Systems', 70.0), (10, 'Data Structures & Algorithms', 72.0), (10, 'Computer Networks', 68.0), (10, 'Operating Systems', 75.0),
            (11, 'Object Oriented Programming', 65.0), (11, 'Database Management Systems', 70.0), (11, 'Data Structures & Algorithms', 68.0), (11, 'Computer Networks', 62.0), (11, 'Operating Systems', 66.0),
            (12, 'Object Oriented Programming', 38.0), (12, 'Database Management Systems', 42.0), (12, 'Data Structures & Algorithms', 40.0), (12, 'Computer Networks', 36.0), (12, 'Operating Systems', 41.0)
        ]
        cursor.executemany('INSERT INTO marks (student_id, subject, marks_obtained, max_marks) VALUES (?, ?, ?, 100.0)', seed_marks)

        # 4. Attendance
        seed_attendance = [
            (1, 120, 108), (2, 120, 114), (3, 120, 85), (4, 120, 102),
            (5, 120, 92), (6, 100, 88), (7, 120, 80), (8, 120, 72),
            (9, 100, 94), (10, 120, 100), (11, 120, 110), (12, 100, 70)
        ]
        cursor.executemany('INSERT INTO attendance (student_id, total_classes, attended_classes) VALUES (?, ?, ?)', seed_attendance)
        conn.commit()

    conn.close()

def compute_grades(percentage, marks_list):
    all_passed = all(m >= 35.0 for m in marks_list) if marks_list else False
    if not all_passed or percentage < 40.0:
        return 'F', 'FAIL', 'Fail / Needs Improvement'
    if percentage >= 90.0:
        return 'O', 'PASS', 'First Class with Exemplary Distinction'
    elif percentage >= 80.0:
        return 'A+', 'PASS', 'First Class with Distinction'
    elif percentage >= 70.0:
        return 'A', 'PASS', 'First Class with Higher Grade'
    elif percentage >= 60.0:
        return 'B', 'PASS', 'First Class'
    elif percentage >= 50.0:
        return 'C', 'PASS', 'Higher Second Class'
    else:
        return 'D', 'PASS', 'Pass Class'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            flash('Please sign in to access the ERP Portal.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ------------------------------------------------------------------------------
# ROUTES & STATIC ALIASES
# ------------------------------------------------------------------------------

@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory(os.path.join(app.static_folder, 'images'), filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.static_folder, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.static_folder, 'js'), filename)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()

        # Check credentials (admin/admin123 or teacher/teacher123)
        if user and ((user['password'] == password) or (username == 'admin' and password == 'admin123') or (username == 'teacher' and password == 'teacher123')):
            session['username'] = user['username']
            session['role'] = user['role']
            flash(f'Welcome back, {user["username"]}! Successfully authenticated.', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been securely signed out.', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    cursor = conn.cursor()

    # Total students
    cursor.execute('SELECT COUNT(*) FROM students')
    total_students = cursor.fetchone()[0]

    # Department distribution
    cursor.execute('SELECT department, COUNT(*) as count FROM students GROUP BY department')
    dept_rows = cursor.fetchall()
    dept_labels = [r['department'] for r in dept_rows]
    dept_counts = [r['count'] for r in dept_rows]
    departments_count = len(dept_labels)

    # Attendance stats
    cursor.execute('SELECT total_classes, attended_classes FROM attendance')
    att_rows = cursor.fetchall()
    total_att_pct = 0.0
    shortage_count = 0
    for r in att_rows:
        pct = (r['attended_classes'] / r['total_classes'] * 100) if r['total_classes'] > 0 else 0
        total_att_pct += pct
        if pct < 75.0:
            shortage_count += 1
    avg_attendance = round(total_att_pct / len(att_rows), 1) if att_rows else 0.0

    # Results stats
    cursor.execute('SELECT id FROM students')
    student_ids = [r['id'] for r in cursor.fetchall()]
    passed_count = 0
    failed_count = 0
    for sid in student_ids:
        cursor.execute('SELECT marks_obtained FROM marks WHERE student_id = ?', (sid,))
        m_list = [row['marks_obtained'] for row in cursor.fetchall()]
        pct = (sum(m_list) / 500 * 100) if m_list else 0.0
        _, status, _ = compute_grades(pct, m_list)
        if status == 'PASS':
            passed_count += 1
        else:
            failed_count += 1

    pass_rate = round((passed_count / total_students * 100), 1) if total_students > 0 else 0.0

    # Recent students
    cursor.execute('''
        SELECT s.*, a.total_classes, a.attended_classes 
        FROM students s 
        LEFT JOIN attendance a ON s.id = a.student_id 
        ORDER BY s.id DESC LIMIT 6
    ''')
    recent_students = []
    for s in cursor.fetchall():
        total = s['total_classes'] or 0
        attended = s['attended_classes'] or 0
        att_pct = round((attended / total * 100), 1) if total > 0 else 0.0

        cursor.execute('SELECT marks_obtained FROM marks WHERE student_id = ?', (s['id'],))
        m_list = [row['marks_obtained'] for row in cursor.fetchall()]
        pct = (sum(m_list) / 500 * 100) if m_list else 0.0
        _, status, _ = compute_grades(pct, m_list)

        recent_students.append({
            'id': s['id'],
            'student_id': s['student_id'],
            'name': s['name'],
            'email': s['email'],
            'department': s['department'],
            'class_year': s['class_year'],
            'attendance_pct': att_pct,
            'result_status': status
        })

    conn.close()

    stats = {
        'total_students': total_students,
        'departments_count': departments_count,
        'avg_attendance': avg_attendance,
        'passed_count': passed_count,
        'failed_count': failed_count,
        'pass_rate': pass_rate,
        'shortage_count': shortage_count
    }

    return render_template(
        'dashboard.html',
        active_page='dashboard',
        stats=stats,
        dept_labels=dept_labels,
        dept_counts=dept_counts,
        recent_students=recent_students
    )

@app.route('/students')
@login_required
def students_list():
    query = request.args.get('query', '').strip()
    selected_dept = request.args.get('department', '').strip()

    conn = get_db()
    cursor = conn.cursor()

    sql = 'SELECT * FROM students WHERE 1=1'
    params = []

    if query:
        sql += ' AND (student_id LIKE ? OR name LIKE ? OR email LIKE ?)'
        like_q = f'%{query}%'
        params.extend([like_q, like_q, like_q])

    if selected_dept:
        sql += ' AND department = ?'
        params.append(selected_dept)

    sql += ' ORDER BY id ASC'
    cursor.execute(sql, params)
    students = cursor.fetchall()
    conn.close()

    return render_template(
        'students_list.html',
        active_page='students',
        students=students,
        departments=DEPARTMENTS,
        query=query,
        selected_department=selected_dept
    )

@app.route('/students/search')
@login_required
def students_search():
    query = request.args.get('query', '').strip()
    selected_dept = request.args.get('department', '').strip()
    has_searched = bool(query or selected_dept)

    results = []
    if has_searched:
        conn = get_db()
        cursor = conn.cursor()
        sql = 'SELECT * FROM students WHERE 1=1'
        params = []
        if query:
            sql += ' AND (student_id LIKE ? OR name LIKE ? OR email LIKE ?)'
            like_q = f'%{query}%'
            params.extend([like_q, like_q, like_q])
        if selected_dept:
            sql += ' AND department = ?'
            params.append(selected_dept)
        sql += ' ORDER BY id ASC'
        cursor.execute(sql, params)
        results = cursor.fetchall()
        conn.close()

    return render_template(
        'students_search.html',
        active_page='search_students',
        results=results,
        has_searched=has_searched,
        departments=DEPARTMENTS,
        query=query,
        selected_department=selected_dept
    )

@app.route('/students/add', methods=['GET', 'POST'])
@login_required
def student_add():
    if request.method == 'POST':
        student_id = request.form.get('student_id', '').strip()
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        class_year = request.form.get('class_year', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        dob = request.form.get('dob', '').strip()
        gender = request.form.get('gender', '').strip()
        admission_date = request.form.get('admission_date', '').strip()
        address = request.form.get('address', '').strip()

        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO students (student_id, name, department, class_year, email, phone, address, dob, gender, admission_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (student_id, name, department, class_year, email, phone, address, dob, gender, admission_date))
            new_id = cursor.lastrowid

            # Initialize 5 subjects with 0.0
            for sub in SUBJECTS:
                cursor.execute('INSERT INTO marks (student_id, subject, marks_obtained, max_marks) VALUES (?, ?, 0.0, 100.0)', (new_id, sub))

            # Initialize attendance
            cursor.execute('INSERT INTO attendance (student_id, total_classes, attended_classes) VALUES (?, 120, 100)', (new_id,))
            conn.commit()

            flash(f'Student "{name}" ({student_id}) enrolled successfully!', 'success')
            return redirect(url_for('students_list'))
        except sqlite3.IntegrityError as e:
            flash(f'Error: Student ID or Email already exists in the system.', 'error')
        finally:
            conn.close()

    return render_template('student_form.html', active_page='add_student', is_edit=False, student=None)

@app.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def student_edit(id):
    conn = get_db()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        department = request.form.get('department', '').strip()
        class_year = request.form.get('class_year', '').strip()
        email = request.form.get('email', '').strip()
        phone = request.form.get('phone', '').strip()
        dob = request.form.get('dob', '').strip()
        gender = request.form.get('gender', '').strip()
        admission_date = request.form.get('admission_date', '').strip()
        address = request.form.get('address', '').strip()

        cursor.execute('''
            UPDATE students 
            SET name = ?, department = ?, class_year = ?, email = ?, phone = ?, address = ?, dob = ?, gender = ?, admission_date = ?
            WHERE id = ?
        ''', (name, department, class_year, email, phone, address, dob, gender, admission_date, id))
        conn.commit()
        conn.close()

        flash(f'Student details for "{name}" updated successfully.', 'success')
        return redirect(url_for('students_list'))

    cursor.execute('SELECT * FROM students WHERE id = ?', (id,))
    student = cursor.fetchone()
    conn.close()

    if not student:
        flash('Student record not found.', 'error')
        return redirect(url_for('students_list'))

    return render_template('student_form.html', active_page='students', is_edit=True, student=student)

@app.route('/students/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def student_delete(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT name, student_id FROM students WHERE id = ?', (id,))
    st = cursor.fetchone()
    if st:
        cursor.execute('DELETE FROM marks WHERE student_id = ?', (id,))
        cursor.execute('DELETE FROM attendance WHERE student_id = ?', (id,))
        cursor.execute('DELETE FROM students WHERE id = ?', (id,))
        conn.commit()
        flash(f'Student "{st["name"]}" ({st["student_id"]}) and all related marks & attendance were permanently deleted.', 'success')
    conn.close()
    return redirect(url_for('students_list'))

@app.route('/marks')
@login_required
def marks_list():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY id ASC')
    students = cursor.fetchall()

    records = []
    for s in students:
        cursor.execute('SELECT subject, marks_obtained FROM marks WHERE student_id = ?', (s['id'],))
        m_dict = {row['subject']: row['marks_obtained'] for row in cursor.fetchall()}
        
        # Ensure all 5 subjects
        for sub in SUBJECTS:
            if sub not in m_dict:
                m_dict[sub] = 0.0

        total = sum(m_dict.values())
        pct = round((total / 500 * 100), 2)
        grade, status, _ = compute_grades(pct, list(m_dict.values()))

        records.append({
            'id': s['id'],
            'student_id': s['student_id'],
            'name': s['name'],
            'department': s['department'],
            'class_year': s['class_year'],
            'marks': m_dict,
            'total': total,
            'percentage': pct,
            'grade': grade,
            'status': status
        })

    conn.close()
    return render_template('marks_list.html', active_page='marks', records=records)

@app.route('/marks/entry/<int:id>', methods=['GET', 'POST'])
@login_required
def marks_entry(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students WHERE id = ?', (id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        flash('Student record not found.', 'error')
        return redirect(url_for('marks_list'))

    if request.method == 'POST':
        for i in range(len(SUBJECTS)):
            sub_name = request.form.get(f'subject_name_{i}', '').strip()
            score_val = float(request.form.get(f'subject_{i}', 0.0) or 0.0)
            score_val = max(0.0, min(100.0, score_val))

            cursor.execute('SELECT id FROM marks WHERE student_id = ? AND subject = ?', (id, sub_name))
            existing = cursor.fetchone()
            if existing:
                cursor.execute('UPDATE marks SET marks_obtained = ? WHERE id = ?', (score_val, existing['id']))
            else:
                cursor.execute('INSERT INTO marks (student_id, subject, marks_obtained, max_marks) VALUES (?, ?, ?, 100.0)', (id, sub_name, score_val))

        conn.commit()
        conn.close()
        flash(f'Academic marks for "{student["name"]}" updated successfully!', 'success')
        return redirect(url_for('marks_list'))

    cursor.execute('SELECT subject, marks_obtained FROM marks WHERE student_id = ?', (id,))
    marks_dict = {row['subject']: row['marks_obtained'] for row in cursor.fetchall()}
    conn.close()

    return render_template('marks_entry.html', active_page='marks', student=student, marks_dict=marks_dict)

@app.route('/attendance')
@login_required
def attendance_list():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT s.id, s.student_id, s.name, s.department, s.class_year, s.email,
               a.total_classes, a.attended_classes
        FROM students s
        LEFT JOIN attendance a ON s.id = a.student_id
        ORDER BY s.id ASC
    ''')
    rows = cursor.fetchall()

    records = []
    for r in rows:
        total = r['total_classes'] or 0
        attended = r['attended_classes'] or 0
        pct = round((attended / total * 100), 2) if total > 0 else 0.0

        records.append({
            'id': r['id'],
            'student_id': r['student_id'],
            'name': r['name'],
            'email': r['email'],
            'department': r['department'],
            'class_year': r['class_year'],
            'total_classes': total,
            'attended_classes': attended,
            'percentage': pct
        })

    conn.close()
    return render_template('attendance_list.html', active_page='attendance', records=records)

@app.route('/attendance/entry/<int:id>', methods=['GET', 'POST'])
@login_required
def attendance_entry(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students WHERE id = ?', (id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        flash('Student record not found.', 'error')
        return redirect(url_for('attendance_list'))

    if request.method == 'POST':
        total = int(request.form.get('total_classes', 0) or 0)
        attended = int(request.form.get('attended_classes', 0) or 0)
        attended = min(total, max(0, attended))

        cursor.execute('SELECT id FROM attendance WHERE student_id = ?', (id,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute('UPDATE attendance SET total_classes = ?, attended_classes = ? WHERE id = ?', (total, attended, existing['id']))
        else:
            cursor.execute('INSERT INTO attendance (student_id, total_classes, attended_classes) VALUES (?, ?, ?)', (id, total, attended))

        conn.commit()
        conn.close()
        flash(f'Attendance hours for "{student["name"]}" recorded successfully!', 'success')
        return redirect(url_for('attendance_list'))

    cursor.execute('SELECT * FROM attendance WHERE student_id = ?', (id,))
    att = cursor.fetchone()
    conn.close()

    return render_template('attendance_entry.html', active_page='attendance', student=student, attendance=att)

@app.route('/reports')
@login_required
def reports_list():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM students ORDER BY id ASC')
    students = cursor.fetchall()

    reports = []
    for s in students:
        cursor.execute('SELECT marks_obtained FROM marks WHERE student_id = ?', (s['id'],))
        m_list = [row['marks_obtained'] for row in cursor.fetchall()]
        pct = round((sum(m_list) / 500 * 100), 2) if m_list else 0.0
        grade, status, classification = compute_grades(pct, m_list)

        reports.append({
            'id': s['id'],
            'student_id': s['student_id'],
            'name': s['name'],
            'department': s['department'],
            'class_year': s['class_year'],
            'percentage': pct,
            'grade': grade,
            'status': status,
            'classification': classification
        })

    conn.close()
    return render_template('reports_list.html', active_page='reports', reports=reports)

@app.route('/reports/<int:id>')
@login_required
def marksheet(id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM students WHERE id = ?', (id,))
    student = cursor.fetchone()
    if not student:
        conn.close()
        flash('Student record not found.', 'error')
        return redirect(url_for('reports_list'))

    cursor.execute('SELECT subject, marks_obtained, max_marks FROM marks WHERE student_id = ?', (id,))
    marks_rows = cursor.fetchall()
    marks = [{'subject': r['subject'], 'marks_obtained': r['marks_obtained'], 'max_marks': r['max_marks']} for r in marks_rows]

    # Ensure all subjects present
    existing_subs = {m['subject'] for m in marks}
    for sub in SUBJECTS:
        if sub not in existing_subs:
            marks.append({'subject': sub, 'marks_obtained': 0.0, 'max_marks': 100.0})

    m_list = [m['marks_obtained'] for m in marks]
    total_marks = sum(m_list)
    pct = round((total_marks / 500 * 100), 2)
    grade, result_status, classification = compute_grades(pct, m_list)

    # Attendance
    cursor.execute('SELECT total_classes, attended_classes FROM attendance WHERE student_id = ?', (id,))
    att = cursor.fetchone()
    att_pct = 0.0
    if att and att['total_classes'] > 0:
        att_pct = round((att['attended_classes'] / att['total_classes'] * 100), 2)

    conn.close()

    report_data = {
        'id': student['id'],
        'student_id': student['student_id'],
        'name': student['name'],
        'department': student['department'],
        'class_year': student['class_year'],
        'email': student['email'],
        'phone': student['phone'],
        'dob': student['dob'],
        'gender': student['gender'],
        'admission_date': student['admission_date'],
        'marks': marks,
        'total_marks': total_marks,
        'percentage': pct,
        'grade': grade,
        'result_status': result_status,
        'classification': classification,
        'attendance_pct': att_pct
    }

    return render_template('marksheet.html', active_page='reports', report=report_data)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 8082))
    print("=" * 60)
    print("  APEX INSTITUTE ERP - COLLEGE STUDENT MANAGEMENT SYSTEM")
    print(f"  Running locally on http://localhost:{port}")
    print("  Default Login: admin / admin123")
    print("=" * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
