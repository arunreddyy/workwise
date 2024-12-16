# Workwise

# Summary Statement

This is a comprehensive productivity app designed to help users efficiently track their daily tasks, monitor progress, and boost overall productivity. The app enables users to manage tasks, set priorities, log daily activities, and visualize performance insights through intuitive graphs. By fostering better time management, This helps users identify productivity trends and pinpoint areas for improvement. With its simple yet effective features and user-friendly interface, it is an essential tool for professionals aiming to optimize their workflow and achieve their goals.

### Features
- **Task Creation & Tracking**: Easily create, assign, and monitor tasks.
- **User Roles**: Supports multiple user roles: Employee, Developer, and Admin.
- **Notifications & Reminders**: Set notifications and reminders for tasks.
- **Data Visualization**: Graphical insights into task statuses and progress.
- **Security**: Authentication and user management.

---

## Technologies Used

### **Programming Languages**
- **Python**: Backend development with Flask.
- **HTML**: Structure of the web pages (templates).
- **CSS**: Styling of frontend components.
- **JavaScript**: Interactivity (form validation, input masks).

### **Frameworks**
- **Flask**: Lightweight web framework for routing, templating, and session management.
- **Flask-Login**: Manages user authentication and session handling.
- **Flask-SQLAlchemy**: ORM for interacting with the database.
- **Flask-Migrate**: Handles database migrations.

### **Database**
- **SQLite**: Lightweight relational database for storing tasks and user data.
- **SQLAlchemy**: ORM for seamless database interaction, provides protection against SQL injection

### **Frontend Libraries/Technologies**
- **Bootstrap**: For responsive, mobile-first web design.
- **Inputmask**: For formatting input fields (e.g., phone number).

### **Email/SMTP**
- **Gmail SMTP**: Used for sending email notifications.
- **smtplib**: Python module for integrating email functionality.

### **Visualization/Reporting**
- **Matplotlib**: Used to generate graphical representations of task status.

### **Development/Build Tools**
- **Docker**: Containerization of the application for consistent deployment across environments.
- **Docker Compose**: Defines and runs multi-container Docker applications.

---

## Setup Instructions

### Prerequisites
Ensure you have Python 3.x and Docker installed on your system.

### Installing Dependencies
1. Clone the repository:
   ```bash
   git clone <repository_url>

2. NAvigate to the project directory

    cd workwise

3. Create a virtual environment (optional but recommended)

    python3 -m venv venv

4. Install required Python packages

    pip install -r requirements.txt


### Project Structure

    workwise/                           # Root project directory
│
├── instance/                        # Stores instance-related files (e.g., database)
│   └── tasks_new.db                 # SQLite database file
│
├── migrations/                      # Migration folder for database schema changes
│   ├── alembic.ini                  # Alembic configuration file for migrations
│   ├── env.py                       # Migration environment setup
│   ├── README                       # Description of migration setup
│   ├── script.py.mako               # Template for migration scripts
│   └── versions/                    # Folder containing individual migration versions
│
├── static/                          # Static files like CSS, JS, and images
│
├── templates/                       # HTML templates for the application
│   ├── admin_dashboard.html         # Admin dashboard template
│   ├── create_task.html             # Task creation template
│   ├── create_user.html             # User creation template
│   ├── dashboard.html               # User dashboard template
│   ├── edit_task.html               # Task editing template
│   ├── login.html                   # Login page template
│   ├── register.html                # User registration template
│   ├── reports.html                 # Reports template
│   ├── tasks.html                   # View tasks template
│   ├── task_table.html              # Task table template
│   └── user_table.html              # User table template
│
├── venv/                            # Virtual environment folder
│
├── .gitignore                       # Specifies which files to ignore in Git
├── app.py                           # Main application file (Flask app)
├── compose.yml                      # Docker Compose configuration
├── Dockerfile                       # Dockerfile for the application
├── README.md                        # Project documentation
└── requirements.txt                 # Python dependencies

### Directory Descriptions:

- instance/: Stores instance-specific files, including the SQLite database.

- migrations/: Contains scripts for database migrations, created by Flask-Migrate.

- static/: Holds static assets like CSS, JS, and images.

- templates/: Contains all HTML templates used for rendering pages.

- venv/: The virtual environment where Python dependencies are installed.

- __pycache__/: Python’s cache directory for compiled bytecode files.

- app.py: Main entry point for the Flask app where routes and logic are defined.

- compose.yml: Defines the multi-container Docker application setup.

- Dockerfile: Instructions for building the Docker image for the application.

- README.md: Project documentation outlining setup, features, and usage.

- requirements.txt: A list of required Python packages for the application.


### Running the Application

- **Running the Flask App**

    Navigate to project folder whenre app.py 

        cd workwise

        python app.py
    
- **Visit the app the browser**

        http://127.0.0.1:5000/


### Running with docker

- **build and start the containers**

    docker compose up --build