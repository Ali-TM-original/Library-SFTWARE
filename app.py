from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library.db"

# initialize db
db = SQLAlchemy(app)


# create db model
class Lib(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime)

    def __repr__(self):
        return '<id %r>' %self.id

@app.route("/home", methods=["POST", "GET"])
def home():
    title = "Home"
    if request.method == "POST":
        name = request.form.get("book_name")
        author = request.form.get("author_name")
        barcode = request.form.get("barcode")
        add_db = Lib(name=name, author=author, barcode=barcode)
        try:
            db.session.add(add_db)
            db.session.commit()
            return redirect(url_for('home'))
        except:    
            return f"{name}|{author}|{barcode}"
    elif request.method == "GET":
        try:
            if session['email'] == 'root@root' and session['pass'] == "root":
                return render_template("newhome.html", title=title)
            elif session['email'] is None and session['pass'] is None:
                return redirect(url_for('login'))   
            else:
                return redirect(url_for('login'))
        except KeyError:
            return redirect(url_for('login'))       


@app.route("/about")
def about():
    title = "About"
    return render_template("about.html", title=title)


@app.route("/")
def login():
    title = "Login"
    return render_template("login.html", title=title)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/db")
def databs():
    data = Lib.query.order_by(Lib.id)
    return render_template("data.html", data=data)

@app.route("/delete/<int:id>")
def delete(id):
    deleted = Lib.query.get_or_404(id)
    try:
        db.session.delete(deleted)
        db.session.commit()
        return redirect(url_for('databs')) 
    except:
        return redirect(url_for('home'))    

@app.route("/update/<int:id>")
def update(id):
    return redirect(url_for('home'))
       
@app.route("/form", methods=["POST"])
def form():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("pass")
        print(f"{email}  |||   {password}")
        """
        if email is None and password is None:
            return redirect(url_for('login'))
        elif email != None and password != None:
        return redirect(url_for('home'))"""
        if email == '' and password == '':
            return redirect(url_for('login'))
        elif email is not None and password is not None:
            session["email"] = email
            session["pass"] = password
            return redirect(url_for('home'))
    else:
        return "HOLA"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def login_error(e):
    return "Ahh you are not logged in"
