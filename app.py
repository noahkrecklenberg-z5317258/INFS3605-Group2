from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__, template_folder="Templates")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    metric = db.Column(db.String(200), nullable=False)
    KPI = db.Column(db.String(200), nullable=False)
    outcome = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(KPI=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        tasks = Todo.query.order_by(Todo.date).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except:
        return ' There was a problem'

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.KPI = request.form['KPI']
        try:
            db.session.commit()
            return redirect('/')
        except:
            'There was an issue'
    else:
       return render_template('update.html', task=task)


@app.route('/add', methods = ['GET', 'POST'])
def add():
    if request.method == 'POST':
        task_KPI = request.form.form['KPI']
        new_KPI = Todo(KPI = task_KPI)

        task_metric = request.form['metric']
        new_metric = Todo(metric = task_metric)

        task_outcome = request.form['outcome']
        new_outcome = Todo(outcome = task_outcome)
        try:
            db.session.add(new_KPI)
            db.session.add(new_metric)
            db.session.add(new_outcome)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        return render_template('add.html')

@app.route('/launchaddscreen')
def launch():
    return render_template('add.html')

    
if __name__ == "__main__":
    app.run(debug=True)

