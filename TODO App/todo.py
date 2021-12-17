from flask import Flask,request,redirect,url_for

from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/Dede/OneDrive/Masaüstü/TODO App/todo.db'  # Veritabanımızın todo.db nin olduğunu dizini ile bağ kurmasını sağlıyoruz
db = SQLAlchemy(app)
@app.route("/")
def index():
    todos = Todo.query.all() # Listenin içinde sözlük halinde veritabanındaki verileri alıyorum.
    
    return render_template("index.html",todos=todos)

# Güncelle
@app.route("/complete/<string:id>")
def complete(id):
    todoid = Todo.query.filter_by(id = id).first() # İd'si id olan veriyi alıp objeye atıyacak
    todoid.complete = not todoid.complete # Ters çeviriyor.

    db.session.commit()

    return redirect(url_for("index"))
# Silme
@app.route("/delete/<string:id>")
def delete(id):
    silme = Todo.query.filter_by(id=id).first() 
    db.session.delete(silme)
    db.session.commit()
    return redirect(url_for("index"))



@app.route("/add",methods = ["POST"])
def add():
    başlik = request.form.get("title") # İndex.html deki input alanından bilgiyi alır.
    newTodo = Todo(title = başlik, complete = False) # Veritabanına basit bir şekilde eklenmesi için obje kurulur.
    db.session.add(newTodo) # Veritabanına ekleme komutunu çalıştırırız.    
    db.session.commit()  # Güncelleme işlemi yapılır.

    return redirect(url_for("index"))


class Todo(db.Model): # ORM ' nin içindeki modelden sınıf oluşturuyoruz
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean) # True ve False değer alacağı için boolean kullanılıyor.


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
