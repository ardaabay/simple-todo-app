from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from forms import TaskForm
from models import db, Task

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)

def create_tables():
    db.create_all()

def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)

def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(title=form.title.data, description=form.description.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_task.html', form=form)

def edit_task(task_id):
    task = Task.query.get(task_id)
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_task.html', form=form, task=task)

def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
