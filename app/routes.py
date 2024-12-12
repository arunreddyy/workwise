from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import db, Task

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def dashboard():
    filter_status = request.args.get('filter', 'All')
    if filter_status == 'Completed':
        tasks = Task.query.filter_by(status='Complete').all()
    elif filter_status == 'Pending':
        tasks = Task.query.filter_by(status='Pending').all()
    else:
        tasks = Task.query.all()
    return render_template('dashboard.html', tasks=tasks, filter_status=filter_status)

@bp.route('/add', methods=['POST'])
@login_required
def add_task():
    if current_user.role not in ['admin', 'dev']:
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    task_name = request.form.get('task_name')
    if task_name:
        new_task = Task(name=task_name)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('main.dashboard'))

@bp.route('/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
    if current_user.role != 'admin':
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.name = request.form.get('task_name')
        db.session.commit()
        return redirect(url_for('main.dashboard'))
    return render_template('edit_task.html', task=task)

@bp.route('/update_status/<int:task_id>', methods=['POST'])
@login_required
def update_status(task_id):
    task = Task.query.get_or_404(task_id)
    task.status = 'Complete' if task.status == 'Pending' else 'Pending'
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@bp.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    if current_user.role != 'admin':
        flash('Permission denied.', 'danger')
        return redirect(url_for('main.dashboard'))

    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('main.dashboard'))
