from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory task storage
tasks = []

# Home route - Dashboard
@app.route('/')
def dashboard():
    return render_template('dashboard.html', tasks=tasks)

# Add Task route
@app.route('/add', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')
    if task_name:
        tasks.append({'name': task_name, 'status': 'Pending'})
    return redirect(url_for('dashboard'))

# Edit Task route
@app.route('/edit/<int:task_index>', methods=['GET', 'POST'])
def edit_task(task_index):
    if request.method == 'POST':
        updated_name = request.form.get('task_name')
        if updated_name and 0 <= task_index < len(tasks):
            tasks[task_index]['name'] = updated_name
        return redirect(url_for('dashboard'))
    
    task_to_edit = tasks[task_index] if 0 <= task_index < len(tasks) else None
    return render_template('edit_task.html', task=task_to_edit, task_index=task_index)

# Delete Task route
@app.route('/delete/<int:task_index>', methods=['POST'])
def delete_task(task_index):
    if 0 <= task_index < len(tasks):
        tasks.pop(task_index)
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
