from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)                   #Config same as in video but with "+pymysql" after the mysql init.
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}/{}".format(
    "huappyDee",                                                        #username
    "MasterPassword14",                                                 #password
    "project-database.cciooaq0e4do.us-east-1.rds.amazonaws.com",        #RDS Endpoint    
    "project-database",                                                 #Database name
)
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    reward = db.Column(db.String(250))
    date_to_complete = db.Column(db.DateTime, nullable = False)
    is_complete = db.Column(db.String(20))

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_reward = request.form['reward']
        task_date_to_complete = request.form['complete_by']
        new_task = Todo(content=task_content, reward = task_reward, date_to_complete= task_date_to_complete, is_complete= 'Incompelte')

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return f'There was an issue adding your task: {new_task}, \n{new_task.content}, \n{new_task.date_created}, \n{new_task.reward}, \n{new_task.date_to_complete}, \n{new_task.is_complete}'

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        completeness = request.form.get('is_complete')
        task.reward = request.form["reward"]
        task.complete_by = request.form['complete_by']

        if completeness == "true":
            task.is_complete = "Complete"
        else:
            task.is_complete = "Incomplete"

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
                                         
