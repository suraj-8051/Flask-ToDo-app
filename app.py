from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDo(db.Model):
    srno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    desc = db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.srno} - {self.title}"
    
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
       title = request.form['title']
       desc = request.form['desc']
       todo = ToDo(title = title, desc=desc)
       db.session.add(todo)
       db.session.commit()

    allToDo = ToDo.query.all()
    return render_template('index.html', allToDo=allToDo)



@app.route('/show')
def products():
    allToDo = ToDo.query.all()
    print(allToDo)
    return 'this is products page'


@app.route('/delete/<int:srno>')
def delete(srno):
    todo = ToDo.query.filter_by(srno=srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


@app.route('/update/<int:srno>', methods=["GET", "POST"])
def update(srno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = ToDo.query.filter_by(srno=srno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = ToDo.query.filter_by(srno=srno).first()
    return render_template('update.html', todo=todo)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)
