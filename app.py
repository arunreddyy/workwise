from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
#from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

# Set the secret key to enable CSRF protection
app.config['SECRET_KEY'] = 'password12345'  # Change this to a strong key
#csrf = CSRFProtect(app)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), default='Pending')

    def __repr__(self):
        return f'<Task {self.id} - {self.name}>'

# Initialize database directly at app startup
with app.app_context():
    db.create_all()


# Home route - Dashboard with filtering
@app.route('/')
def dashboard():
    filter_status = request.args.get('filter', 'All')
    if filter_status == 'Completed':
        tasks = Task.query.filter_by(status='Complete').all()
    elif filter_status == 'Pending':
        tasks = Task.query.filter_by(status='Pending').all()
    else:
        tasks = Task.query.all()
    return render_template('dashboard.html', tasks=tasks, filter_status=filter_status)

# Add Task route
@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    if task_name:
        new_task = Task(name=task_name)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('dashboard'))

# Edit Task route
@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.name = request.form.get('task_name')
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('edit_task.html', task=task)

# Update Task Status
@app.route('/update_status/<int:task_id>', methods=['POST'])
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = 'Complete' if task.status == 'Pending' else 'Pending'
    db.session.commit()
    return redirect(url_for('dashboard'))

# Delete Task route
@app.route('/delete/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
