# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "{} - {}".format(self.sno, self.title)


@app.route('/', methods=['GET', 'POST'])
def create_record():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        if len(title) != 0 and len(desc) != 0:
            todo = Todo(title=title, desc=desc)
            db.session.add(todo)
            db.session.commit()
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)


# @app.route('/show')
# def show_all():
#     allTodo = Todo.query.all()
#     print(allTodo)
#     return "All todos printed."


@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        todo.date_created = datetime.now()
        if len(title) != 0 and len(desc) != 0:
            db.session.add(todo)
            db.session.commit()
        return redirect('/')
    update_rec = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=update_rec)


@app.route('/delete/<int:sno>')
def delete(sno):
    del_rec = Todo.query.filter_by(sno=sno).first()
    db.session.delete(del_rec)
    db.session.commit()
    return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
