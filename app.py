from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import date

app = Flask(__name__)
app.secret_key = "clubmatrix_secret_key"

# -----------------------------
# Database Connection
# -----------------------------
def get_db_connection():
    conn = sqlite3.connect('events.db')
    conn.row_factory = sqlite3.Row
    return conn

conn = sqlite3.connect('events.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        email TEXT,
        password TEXT,
        role TEXT
    )
    """)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        name TEXT,
        course TEXT,
        branch TEXT,
        semester TEXT,
        year TEXT,
        admission_no TEXT,
        reg_no TEXT
    )
    """)

    # CLUBS TABLE
cursor.execute("""
    CREATE TABLE IF NOT EXISTS clubs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        club_name TEXT,
        description TEXT,
        contact TEXT,
        faculty TEXT,
        established_year TEXT
    )
    """)

    # EVENT TABLE
cursor.execute("""
    CREATE TABLE IF NOT EXISTS event (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        club TEXT,
        description TEXT,
        date TEXT,
        time TEXT,
        mode TEXT,
        venue TEXT,
        platform TEXT,
        is_paid TEXT,
        payment_amount TEXT,
        gpay_number TEXT,
        participation_type TEXT,
        activity_points TEXT,
        contact_details TEXT,
        qr_code_link TEXT,
        club_id INTEGER
    )
    """)
conn.commit()
conn.close()


# -----------------------------
# Landing Page
# -----------------------------
@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        conn = get_db_connection()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role=?",
            (username, password, role)
        ).fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']
            session['role'] = user['role']

            if role == 'student':
                return redirect('/student')
            else:
                return redirect('/club')

        else:
            return render_template('login.html', error="Invalid username, password or role.")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO users (username, email, password, role) VALUES (?, ?, ?, ?)",
                       (username, email, password, role))

        conn.commit()

        user_id = cursor.lastrowid
        conn.close()

        session['user_id'] = user_id
        session['role'] = role

        if role == 'student':
            return redirect('/student/details')
        else:
            return redirect('/club/details')

    return render_template('signup.html')

@app.route('/student/details', methods=['GET', 'POST'])
def student_details():
    if session.get('role') != 'student':
        return redirect('/login')

    if request.method == 'POST':
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO students (user_id, name, course, branch, semester, year, admission_no, reg_no)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            session['user_id'],
            request.form['name'],
            request.form['course'],
            request.form['branch'],
            request.form['semester'],
            request.form['year'],
            request.form['admission_no'],
            request.form['reg_no']
        ))

        conn.commit()
        conn.close()

        return redirect('/student')

    return render_template('student_details.html')

@app.route('/club/details', methods=['GET', 'POST'])
def club_details():
    if session.get('role') != 'club':
        return redirect('/login')

    if request.method == 'POST':
        conn = sqlite3.connect('events.db')
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clubs (user_id, club_name, description, contact, faculty, established_year)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            session['user_id'],
            request.form['club_name'],
            request.form['description'],
            request.form['contact'],
            request.form['faculty'],
            request.form['established_year']
        ))

        conn.commit()
        conn.close()

        return redirect('/club')

    return render_template('club_details.html')

# -----------------------------
# Student Dashboard
# -----------------------------
@app.route('/student')
def student_dashboard():

    # 🔐 Security Check
    if 'role' not in session or session['role'] != 'student':
        return redirect('/login')

    tab = request.args.get('tab', 'loading')

    conn = get_db_connection()

    # ✅ Get logged in student details
    student = conn.execute(
        'SELECT * FROM students WHERE user_id = ?',
        (session['user_id'],)
    ).fetchone()

    # ✅ Get events
    events = conn.execute('SELECT * FROM event').fetchall()

    # ✅ Get clubs
    clubs = conn.execute('SELECT DISTINCT club FROM event').fetchall()

    conn.close()

    today = date.today().isoformat()

    today_events = []
    upcoming = []
    past = []

    for event in events:
        if event['date'] == today:
            today_events.append(event)
        elif event['date'] > today:
            upcoming.append(event)
        else:
            past.append(event)

    upcoming.sort(key=lambda x: (x['date'], x['time']))
    past.sort(key=lambda x: (x['date'], x['time']), reverse=True)

    return render_template(
        'student_dashboard.html',
        tab=tab,
        today_events=today_events,
        upcoming=upcoming,
        past=past,
        clubs=clubs,
        student=student
    )



@app.route('/event/<int:event_id>')
def event_detail(event_id):
    source = request.args.get('source', 'student')

    conn = get_db_connection()
    event = conn.execute(
        'SELECT * FROM event WHERE id = ?',
        (event_id,)
    ).fetchone()
    conn.close()

    if source == 'club':
        return render_template('event_detail.html', event=event)
    else:
        return render_template('event_detail_student.html', event=event)


@app.route('/student/club/<club_name>')
def student_club_view(club_name):

    # 🔐 Optional security check
    if 'role' not in session or session['role'] != 'student':
        return redirect('/login')

    conn = get_db_connection()

    # Get all events of this club
    events = conn.execute(
        "SELECT * FROM event WHERE club = ?",
        (club_name,)
    ).fetchall()

    conn.close()

    today = date.today().isoformat()

    today_events = []
    upcoming = []
    past = []

    for event in events:
        if event['date'] == today:
            today_events.append(event)
        elif event['date'] > today:
            upcoming.append(event)
        else:
            past.append(event)

    # Sorting
    today_events.sort(key=lambda x: (x['date'], x['time']))
    upcoming.sort(key=lambda x: (x['date'], x['time']))
    past.sort(key=lambda x: (x['date'], x['time']), reverse=True)

    return render_template(
        "student_club_view.html",
        club_name=club_name,
        today_events=today_events,
        upcoming=upcoming,
        past=past
    )



# -----------------------------
# Club Dashboard
# -----------------------------
@app.route('/club')
def club_dashboard():
    if 'role' not in session or session['role'] != 'club':
        return redirect('/login')


    tab = request.args.get('tab', 'loading')

    conn = get_db_connection()
    club = conn.execute(
        "SELECT * FROM clubs WHERE user_id = ?",
        (session['user_id'],)
    ).fetchone()
    events = conn.execute(
    "SELECT * FROM event WHERE club_id = ?",
    (session['user_id'],)
    ).fetchall()
    conn.close()

    today = date.today().isoformat()

    today_events = []
    upcoming_events = []
    past_events = []

    for event in events:
        if event['date'] == today:
            today_events.append(event)
        elif event['date'] > today:
            upcoming_events.append(event)
        else:
            past_events.append(event)

    # Sort by date + time properly
    today_events.sort(key=lambda x: (x['date'], x['time']))
    upcoming_events.sort(key=lambda x: (x['date'], x['time']))
    past_events.sort(key=lambda x: (x['date'], x['time']), reverse=True)

    return render_template(
        'club_dashboard.html',
        tab=tab,
        today_events=today_events,
        upcoming_events=upcoming_events,
        past_events=past_events,
        events=events,
        club=club
    )

@app.route("/favicon.ico")
def favicon():
    return "", 200

# -----------------------------
# Add Event (Admin Mode)
# -----------------------------
@app.route('/admin/add', methods=('GET', 'POST'))
def add_event():
    if request.method == 'POST':
        name = request.form['name']
        club = request.form['club']
        description = request.form['description']
        date_val = request.form['date']
        time = request.form['time']

        mode = request.form['mode']
        venue = request.form['venue']
        platform = request.form['platform']

        is_paid = request.form['is_paid']
        payment_amount = request.form['payment_amount']
        gpay_number = request.form['gpay_number']

        participation_type = request.form['participation_type']
        activity_points = request.form['activity_points']

        contact_details = request.form['contact_details']
        qr_code_link = request.form['qr_code_link']
        club_id=session['user_id']
        conn = get_db_connection()
        conn.execute(
            '''
            INSERT INTO event (
                name, club, description, date, time,
                mode, venue, platform,
                is_paid, payment_amount, gpay_number,
                participation_type, activity_points,
                contact_details, qr_code_link,club_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
            ''',
            (
                name, club, description, date_val, time,
                mode, venue, platform,
                is_paid, payment_amount, gpay_number,
                participation_type, activity_points,
                contact_details, qr_code_link,club_id
            )
        )
        conn.commit()
        conn.close()

        return redirect('/club')

    return render_template('add_event.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')


@app.route('/test_home')
def test_home():
    # Temporary route to quickly verify template rendering without login
    sample_student = {
        'name': 'Test Student',
        'course': 'B.Tech',
        'branch': 'CSE',
        'semester': '5',
        'year': '3',
        'admission_no': 'A123',
        'reg_no': 'R123'
    }
    return render_template(
        'home.html',
        tab='loading',
        today_events=[],
        upcoming=[],
        past=[],
        clubs=[],
        student=sample_student
    )
# -----------------------------
# Run App
# -----------------------------
if __name__ == '__main__':
    app.run()