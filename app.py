from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///wowtodo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable= False)
    desc = db.Column(db.String(400), nullable= False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"
    
@app.route("/", methods = ['GET', 'POST'])
def main_page():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc) #Creates a new instance of the Todo model (defined elsewhere in your app) using the values provided by the user (title and desc).
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() # getting all todos
    return render_template('index.html', allTodo = allTodo) # rendering index.html on "/" and passing todo list to the index.html page to represnt on it

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route("/update/<int:sno>", methods = ['GET', 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first() # passing the particular sno from the query to delete
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template("update.html", todo = todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()# passing the particular sno from the query to delete
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True ,port=8000)   