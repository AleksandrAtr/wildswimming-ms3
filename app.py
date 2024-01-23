import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/get_posts")
def get_posts():
    posts = list(mongo.db.posts.find())
    image_url = url_for('static', filename='images/test.jpg')
    return render_template("blog.html", posts=posts, image_url=image_url)


@app.route("/create_post", methods = ["GET","POST"])
def create_post():
    if request.method == "POST":
        title_input = request.form.get('title')
        textarea_content = request.form.get('content')
        # verify title input
        if not title_input or len(title_input) > 50:
            flash("Title shall not be more than 50", "error")
            return render_template('create_post.html', title_input=title_input, textarea_content=textarea_content)
        # verify content input
        if not textarea_content or len(textarea_content) > 500:
            flash("Post content shall not be more than 500", "error")
            return render_template('create_post.html', title_input=title_input, textarea_content=textarea_content)
        
        # get user input and user details
        title = request.form['title']
        content = request.form['content']
        keywords = [tag.strip() for tag in request.form['keywords'].split(',') if tag.strip()]
        # get user details
        user_details = mongo.db.users.find_one({"username": session["user"]})
        # assign user details to author
        author = {
        'id': str(user_details["_id"]),
        'username': user_details["username"]
        }
        # create a date stamp with a specific format
        date_stamp = datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')
        # 
        save_post(title, content, author, keywords, date_stamp)
    # if GET method check if user in session if not redirect to log in
    if "user" in session:
        return render_template("create_post.html")
    else:
        flash("Log in to post", "error")
        return redirect(url_for("login"))


# save post to mongoDB function
def save_post(title, content, author, keywords, date_stamp):
    post_data = {
        'title': title,
        'content': content,
        'author': author,
        'keywords': keywords,
        'created_at': date_stamp
    }
    # Insert the post into the MongoDB collection
    mongo.db.posts.insert_one(post_data)
    flash("Blog has been posted", "success")
    return redirect(url_for("get_posts"))

@app.route("/get_register", methods = ["GET","POST"])
def get_register():
    if request.method == "POST":
        username = request.form.get('username').lower()
        password = request.form.get('password')
        
        user = mongo.db.users.find_one({'username': username})
        
        if user:
            flash("User already exists, choose another one", "error")
            return redirect(url_for("get_register"))
        
        register = {
            "username": username,
            "password": generate_password_hash(password)
        }
        mongo.db.users.insert_one(register)

        # set a new user to the session cookie
        session["user"] = username
        flash("Registration Successful!", "success")
        return redirect(url_for("profile"))

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # Assign form inputs to new variables
        username = request.form.get('username').lower()
        password = request.form.get('password')

        user_id = mongo.db.users.find_one({'username': username})

        if user_id and check_password_hash(user_id['password'], password):
            flash('Login successful!', 'success')
            session["user"] = request.form.get("username").lower()
            return redirect(url_for("profile", username=session["user"].capitalize()))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    # Check if the 'user' is in the session to direct to profile page
    if "user" in session:
        user_id = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        return render_template('profile.html', username=user_id.capitalize())

    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    # Clear the 'user' key from the session to log out the user
    session.pop('user', None)
    flash('You have logged out', 'success')
    
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
    
