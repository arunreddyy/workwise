from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configurations
app.config['SECRET_KEY'] = 'password12345'
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'tasks.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)

# Ensure instance folder exists
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

# Create all tables
with app.app_context():
    db.create_all()

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
    user = db.relationship('User', backref='tasks', lazy=True)

# Load user callback
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
@login_required
def dashboard():
    filter_status = request.args.get('filter', 'All')

    if current_user.role == 'admin':  # Admin sees all tasks
        tasks = Task.query.all() if filter_status == 'All' else Task.query.filter_by(status=filter_status).all()
    else:  # Other users see only their tasks
        tasks = Task.query.filter_by(assigned_to=current_user.id) if filter_status == 'All' else Task.query.filter_by(status=filter_status, assigned_to=current_user.id).all()

    users = User.query.all() if current_user.role == 'admin' else []  # Only admin sees users for task assignment
    return render_template('dashboard.html', tasks=tasks, filter_status=filter_status, users=users)

@app.route('/add', methods=['POST'])
@login_required
def add_task():
    if current_user.role not in ['admin', 'dev']:
        flash('Permission denied.', 'danger')
        return redirect(url_for('dashboard'))

    task_name = request.form.get('task_name')
    assigned_to = request.form.get('assigned_to')

    if task_name:
        assigned_user = assigned_to if current_user.role == 'admin' else current_user.id
        new_task = Task(name=task_name, assigned_to=assigned_user)
        db.session.add(new_task)
        db.session.commit()
        flash('Task added successfully!', 'success')
    else:
        flash('Task name cannot be empty.', 'danger')

    return redirect(url_for('dashboard'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role != 'admin' and task.assigned_to != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        task.name = request.form.get('task_name')
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_task.html', task=task)

@app.route('/update_status/<int:task_id>', methods=['POST'])
@login_required
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role != 'admin' and task.assigned_to != current_user.id:
        flash('Permission denied.', 'danger')
        return redirect(url_for('dashboard'))

    task.status = 'Complete' if task.status == 'Pending' else 'Pending'
    db.session.commit()
    flash('Task status updated!', 'success')
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
    app.run(debug=True)
