from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "segredo123"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///agrosustent.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def current_user():
    if "user_id" in session:
        return User.query.get(session["user_id"])
    return None

@app.route('/')
def index():
    produtos = Product.query.order_by(Product.created_at.desc()).all()
    return render_template("index.html", title="Início", user=current_user(), produtos=produtos)

@app.route('/sobre')
def sobre():
    return render_template("sobre.html", title="Sobre", user=current_user())

@app.route('/contato')
def contato():
    return render_template("contato.html", title="Contato", user=current_user())

@app.route('/cadastro', methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado!", "error")
        else:
            user = User(name=name, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash("Cadastro realizado com sucesso!", "success")
            return redirect(url_for("login"))

    return render_template("cadastro.html", title="Cadastro", user=current_user())

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id
            flash("Login realizado com sucesso!", "success")
            return redirect(url_for("index"))
        else:
            flash("E-mail ou senha inválidos!", "error")

    return render_template("login.html", title="Login", user=current_user())

@app.route('/logout')
def logout():
    session.pop("user_id", None)
    flash("Logout realizado!", "info")
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

    

    
