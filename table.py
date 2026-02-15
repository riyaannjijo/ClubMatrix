import sqlite3

# Connect to database
conn = sqlite3.connect('events.db')
cursor = conn.cursor()

import sqlite3

def delete_user(username):
    conn = sqlite3.connect('events.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM users WHERE username = ?", (username,))

    conn.commit()
    conn.close()

    print("User deleted successfully")



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
    qr_code_link TEXT
)
""")
