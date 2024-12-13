import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate  # Import Flask-Migrate
import os
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configurations
app.config['SECRET_KEY'] = 'password12345'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'tasks.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='viewer')  # Roles: admin, dev, viewer

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')
    assigned_to = db.Column(db.Integer, db.ForeignKey('user.id'))  # Link to User table
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), default='Medium')  # High, Medium, Low
    user = db.relationship('User', backref='tasks', lazy=True)

# Load user callback
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# Routes
@app.route('/')
@login_required
def dashboard():
    filter_status = request.args.get('filter', 'All')

    tasks_query = Task.query

    if current_user.role in ['admin', 'dev']:
        if filter_status != 'All':
            tasks_query = tasks_query.filter_by(status=filter_status)
    else:
        tasks_query = tasks_query.filter_by(assigned_to=current_user.id)
        if filter_status != 'All':
            tasks_query = tasks_query.filter_by(status=filter_status)

    tasks = tasks_query.order_by(Task.due_date.asc(), Task.priority.desc()).all()
    users = User.query.all() if current_user.role in ['admin', 'dev'] else []

    return render_template('dashboard.html', tasks=tasks, filter_status=filter_status, users=users)

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    if current_user.role not in ['admin', 'dev']:
        flash('Permission denied.', 'danger')
        return redirect(url_for('dashboard'))

    task_name = request.form.get('task_name')
    assigned_to = request.form.get('assigned_to')
    due_date = request.form.get('due_date')
    priority = request.form.get('priority', 'Medium')

    try:
        due_date = datetime.datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
    except ValueError:
        flash('Invalid date format. Use YYYY-MM-DD.', 'danger')
        return redirect(url_for('dashboard'))

    if task_name:
        new_task = Task(
            name=task_name,
            assigned_to=assigned_to if current_user.role == 'admin' else current_user.id,
            due_date=due_date,
            priority=priority
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')

    return redirect(url_for('dashboard'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role not in ['admin', 'dev'] or (task.assigned_to != current_user.id and current_user.role != 'admin'):
        flash('Permission denied.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        task.name = request.form.get('task_name')
        task.due_date = datetime.datetime.strptime(request.form.get('due_date'), '%Y-%m-%d') if request.form.get('due_date') else None
        task.priority = request.form.get('priority', 'Medium')
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('edit_task.html', task=task)

@app.route('/update_status/<int:task_id>', methods=['POST'])
@login_required
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role not in ['admin', 'dev'] or (task.assigned_to != current_user.id and current_user.role != 'admin'):
        flash('Permission denied.', 'danger')
        return redirect(url_for('dashboard'))

    task.status = 'Completed' if task.status == 'Pending' else 'Pending'
    db.session.commit()
    flash('Task status updated successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role != 'admin':
        flash('Permission denied.', 'danger')
        return redirect(url_for('dashboard'))

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('dashboard'))

@app.route('/reports')
@login_required
def reports():
    if current_user.role != 'admin':
        flash('Permission denied.', 'danger')
        return redirect(url_for('dashboard'))

    tasks = Task.query.all()
    df = pd.DataFrame([{
        'Task Name': task.name,
        'Status': task.status,
        'Assigned To': task.user.username if task.user else 'Unassigned',
        'Due Date': task.due_date,
        'Priority': task.priority
    } for task in tasks])

    # Count tasks by status
    status_counts = df['Status'].value_counts()

    # Plot task status counts
    plt.figure(figsize=(6, 4))
    status_counts.plot(kind='bar', color=['green', 'orange'])
    plt.title('Tasks by Status')
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    chart_base64 = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return render_template(
        'reports.html',
        task_count=len(tasks),
        completed_tasks=status_counts.get('Completed', 0),
        pending_tasks=status_counts.get('Pending', 0),
        chart_base64=chart_base64
    )

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role', 'viewer')

        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, role=role)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
