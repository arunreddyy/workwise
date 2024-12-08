from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Temporary task list to simulate a database
tasks = []

# Dashboard route
@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# Route to display tasks
@app.route('/tasks')
def show_tasks():
    return render_template('tasks.html', tasks=tasks)

# Route to add new tasks
@app.route('/add_task', methods=['POST'])
def add_task():
    task_name = request.form.get('task_name')  # Get task name from form
    if task_name:
        tasks.append({'name': task_name, 'status': 'Pending'})  # Add to task list
    return redirect(url_for('show_tasks'))  # Redirect back to tasks page

if __name__ == '__main__':
    app.run(debug=True)
