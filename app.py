import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/get_posts")
def get_posts():
    posts = mongo.db.posts.find()
    return render_template("posts.html", posts=posts)


@app.route("/get_register", methods = ["GET","POST"])
def get_register():
    if request.method == "POST":
        username = request.form.get('username').lower()
        password = request.form.get('password')
        
        user = mongo.db.users.find_one({'username': username})
        
        if user:
            flash("User already exists, choose another one")
            return redirect(url_for("get_register"))
        
        register = {
            "username": username,
            "password": generate_password_hash(password)
        }
        mongo.db.users.insert_one(register)

        # set a new user to the session cookie
        session["user"] = username
        flash("Registration Successful!")

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username').lower()
        password = request.form.get('password')

        user_id = mongo.db.users.find_one({'username': username})

        if user_id and check_password_hash(user_id['password'], password):
            flash('Login successful!', 'success')
            session["user"] = request.form.get("username").lower()
            redirect(url_for("profile", username=session["user"].capitalize()))
        else:
            flash('Invalid username or password. Please try again.', 'error')

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    user_id = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if session["user"]:
        return render_template('profile.html', username=user_id.capitalize())

    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
    
