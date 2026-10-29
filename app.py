from flask import Flask, render_template, request, redirect, url_for
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)

DATA_DIR = '/app/data'
DATA_FILE = os.path.join(DATA_DIR, 'tasks.json')

os.makedirs(DATA_DIR, exist_ok=True)

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

@app.route('/', methods=['GET', 'POST'])
def index():
    tasks = load_tasks()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        if title:
            new_task = {
                'id': str(uuid.uuid4())[:8],
                'title': title,
                'created_at': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'done': False
            }
            tasks.append(new_task)
            save_tasks(tasks)
        return redirect(url_for('index'))

    return render_template('index.html', tasks=tasks)

@app.route('/delete/<task_id>', methods=['POST'])
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [t for t in tasks if t['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/toggle/<task_id>', methods=['POST'])
def toggle_task(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['done'] = not task['done']
            break
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
