[![img.png](https://i.postimg.cc/wMtXMCQY/img.png)](https://postimg.cc/JHLDddFp)
*Tink-Her-Hack*


# ClubMatrix 🎯

## Basic Details

### Team Name: Individual

### Team Members
- Member 1: Riya - B.Tech Computer Science

### Hosted Project Link
(https://clubmatrix.onrender.com)

### Project Description
ClubMatrix is a centralized event management platform designed for college communities. It bridges the gap between clubs and students by providing a streamlined interface for event creation, discovery, and management across campus organizations.

### The Problem statement
College event coordination is fragmented across multiple platforms - WhatsApp groups, physical posters, and informal announcements. Students frequently miss important events due to information overload and lack of centralization. Clubs struggle with event visibility, attendance tracking, and maintaining organized communication channels with their audience.

### The Solution
ClubMatrix addresses these challenges by providing a unified digital platform where clubs can create and manage events through dedicated dashboards, while students can discover, filter, and explore events through an intuitive interface. The system automatically categorizes events by timeline (Today, Upcoming, Past) and enables club-specific event browsing, creating a transparent and efficient campus event ecosystem.

---

## Technical Details

### Technologies/Components Used

- Languages used: Python, HTML, CSS, JavaScript
- Frameworks used: Flask
- Libraries used: sqlite3, werkzeug, gunicorn
- Tools used: VS Code, Git, GitHub, Render

---

## Features

Key features of my project:
- Feature 1: **Role-Based Authentication System** - Separate login portals for Students and Clubs with secure session management
- Feature 2: **Automatic Event Categorization** - Smart classification of events into Today, Upcoming, and Past based on event dates
- Feature 3: **Club-Specific Dashboards** - Each club has isolated access to create and manage only their own events
- Feature 4: **Student Event Discovery** - Students can browse all events or filter by specific clubs
- Feature 5: **Real-Time Event Updates** - Dynamic rendering of events with persistent SQLite database storage

---

## Implementation

#### Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/clubmatrix.git

# Navigate to project directory
cd clubmatrix

# Install dependencies
pip install -r requirements.txt
```

#### Run
```bash
# Run the Flask application
python app.py

# Access the application at
# http://127.0.0.1:5000
```

---

## Project Documentation

### For Software:

#### Screenshots (Add at least 3)

[![img1.png](https://i.postimg.cc/zfJG0TMr/img1.png)](https://postimg.cc/QFyDMKh4)
*Login page with role selection for Students and Clubs*

[![img2.png](https://i.postimg.cc/3rymXHmV/img2.png)](https://postimg.cc/xq2XQhs3)
*Student dashboard showing categorized events - Today, Upcoming events with filtering options*

[![img4.png](https://i.postimg.cc/RV73dCFD/img4.png)](https://postimg.cc/tYgCCjF3)
*list of clubs in the college*

[![img3.png](https://i.postimg.cc/mgK0r43G/img3.png)](https://postimg.cc/zySdd9Pd)
*event details from student view*

[![img6.png](https://i.postimg.cc/XJ93WJTW/img6.png)](https://postimg.cc/G836JcLg)
*Signup page with role selection for Students and Clubs*

[![img10.png](https://i.postimg.cc/25ZNdyjW/img10.png)](https://postimg.cc/cK0z0sn1)
*Club-specific dashboard displaying event management interface with create/edit capabilities*

[![img7.png](https://i.postimg.cc/CLhYyw7m/img7.png)](https://postimg.cc/0rBhDRLw)
*Event creation form with fields for event name, description, date, time, and location*

[![img12.png](https://i.postimg.cc/02ygWc29/img12.png)](https://postimg.cc/8s9nsd6Y)
event history(past events)

[![img11.png](https://i.postimg.cc/WbWBQgh6/img11.png)](https://postimg.cc/LnPQPqkn)
*event details from club view*

#### Diagrams

**System Architecture:**

![Architecture Diagram](docs/architecture.png)

```
┌─────────────┐
│   User      │
│ (Student/   │
│   Club)     │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│      Flask Application          │
│  ┌──────────────────────────┐  │
│  │   Routes & Controllers   │  │
│  │  - Authentication        │  │
│  │  - Event Management      │  │
│  │  - Dashboard Logic       │  │
│  └────────┬─────────────────┘  │
│           │                     │
│  ┌────────▼─────────────────┐  │
│  │   Business Logic Layer   │  │
│  │  - Event Categorization  │  │
│  │  - Role-Based Access     │  │
│  │  - Data Validation       │  │
│  └────────┬─────────────────┘  │
└───────────┼─────────────────────┘
            │
            ▼
    ┌───────────────┐
    │ SQLite Database│
    │  - users       │
    │  - clubs       │
    │  - events      │
    └───────────────┘
```

*System architecture showing the three-tier structure: User Interface → Flask Application (Routes, Business Logic) → SQLite Database*

**Application Workflow:**

![Workflow](docs/workflow.png)

```
Student Flow:
1. User visits landing page
2. Selects "Student" role
3. Sign up / Log in
4. Access Student Dashboard
5. View categorized events (Today/Upcoming/Past)
6. Filter events by specific club
7. View event details

Club Flow:
1. User visits landing page
2. Selects "Club" role
3. Sign up / Log in with club credentials
4. Access Club Dashboard
5. View club-specific events
6. Create new event
7. Edit/Manage existing events
8. Events automatically visible to students
```

*Complete user workflow demonstrating both student and club user journeys through the application*

---


#### API Documentation

**Base URL:** `http://127.0.0.1:5000` (Local) / `https://clubmatrix.onrender.com` (Production)

##### Endpoints

**GET /**
- **Description:** Login/Signup page with role selection
- **Parameters:** None
- **Response:** HTML page with Student/Club login options

**POST /signup**
- **Description:** User registration for both students and clubs
- **Parameters:**
  - `username` (string): Unique username
  - `password` (string): User password
  - `role` (string): Either 'student' or 'club'
- **Response:**
```json
{
  "status": "success",
  "message": "Account created successfully",
  "redirect": "/login"
}
```

**POST /login**
- **Description:** Authenticates user and creates session
- **Request Body:**
```json
{
  "username": "john_doe",
  "password": "securepass123",
  "role": "student"
}
```
- **Response:**
```json
{
  "status": "success",
  "redirect": "/student" | "/club"
}
```

**GET /student**
- **Description:** Student dashboard with categorized events
- **Authentication:** Required (session-based)
- **Response:** HTML page with Today, Upcoming, and Past events

**GET /club**
- **Description:** Club dashboard with event management tools
- **Authentication:** Required (session-based)
- **Response:** HTML page with club-specific events and creation interface

**POST /admin/add**
- **Description:** Create new event (Club only)
- **Authentication:** Required (Club role)
- **Request Body:**
```json
{
  "event_name": "Tech Workshop",
  "description": "Introduction to AI",
  "event_date": "2026-03-15",
  "event_time": "14:00",
  "location": "Auditorium"
}
```
- **Response:**
```json
{
  "status": "success",
  "message": "Event created successfully",
  "event_id": 42
}
```

**GET /club/<club_name>**
- **Description:** View all events from a specific club (Student view)
- **Parameters:**
  - `club_name` (string): Name of the club
- **Response:** HTML page with club-specific event list

**POST /logout**
- **Description:** Ends user session and logs out
- **Response:**
```json
{
  "status": "success",
  "redirect": "/"
}
```

---

### Database Schema

**users table:**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('student', 'club'))
);
```

**clubs table:**
```sql
CREATE TABLE clubs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    club_name TEXT UNIQUE NOT NULL,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**events table:**
```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    description TEXT,
    event_date TEXT NOT NULL,
    event_time TEXT,
    location TEXT,
    club_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (club_id) REFERENCES clubs(id)
);
```

---

## Project Demo

### Video
[[Add your demo video link here - YouTube, Google Drive, etc.]](https://drive.google.com/file/d/1B-23R5kdEBjpldhwlM5dEXyUNxbGks4S/view?usp=drive_link)

*The video demonstrates:*
- User registration flow for both students and clubs
- Club event creation process
- Student dashboard navigation and event discovery
- Automatic event categorization (Today/Upcoming/Past)
- Club-specific event filtering
- Real-time database updates

### Additional Demos
- Live Site: [https://clubmatrix.onrender.com](https://clubmatrix.onrender.com)
- Demo Credentials:
  - Student: username: `demo_student`, password: `student123`
  - Club: username: `demo_club`, password: `club123`

---

## AI Tools Used (Optional - For Transparency Bonus)

**Tool Used:** ChatGPT / Claude/GEmimi

**Purpose:** Development assistance and debugging
- Debugging SQLite connection issues
- Route optimization suggestions
- Error handling implementation guidance
- Deployment configuration troubleshooting
- SQL query optimization

**Key Prompts Used:**
- "How to implement role-based authentication in Flask with session management"
- "Debug SQLite date comparison for event categorization"
- "Best practices for deploying Flask app on Render with gunicorn"
- "Implement secure password hashing with werkzeug"


**Human Contributions:**
- Complete system architecture and design
- Database schema planning and implementation
- Business logic for event categorization
- Frontend UI/UX design and layout
- Role-based access control logic
- Integration and end-to-end testing
- Deployment setup and configuration
- All custom styling and responsive design

*Note: AI tools were used primarily for debugging assistance and best practice recommendations. All core functionality, architecture decisions, and creative implementation were human-driven.*

---

## Team Contributions

- **Riya**: Full-stack development, database design and implementation, Flask backend architecture, role-based authentication system, event categorization logic, frontend UI/UX design, deployment configuration on Render, project documentation

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**MIT License** - Permissive license allowing commercial use, modification, distribution, and private use with proper attribution.

---

