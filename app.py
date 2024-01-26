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
    """

    """
    img_url = url_for('static', filename='images/cover.jpg')
    return render_template("index.html", img_url=img_url)


@app.route("/get_posts")
def get_posts():
    """
    Route handling function to retrieve and display blog posts.

    This function fetches blog posts from the MongoDB database and renders
    the 'blog.html' template, passing the retrieved posts and a static
    image URL.

    Returns:
    str: Rendered HTML content for the 'blog.html' template.
    """
    post= list(mongo.db.posts.find())
    image_url = url_for('static', filename='images/post_default.jpg')
    return render_template("blog.html", post=post, image_url=image_url)


@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    """
    Route handling function for creating a new blog post.

    If the request method is POST, this function retrieves user input for
    the blog post title, content, and keywords. It then validates the input,
    retrieves user details, and calls the 'save_post' function to save the
    post to the MongoDB collection.

    If the request method is GET, it checks if the user is in session. If not,
    it redirects to the login page. Otherwise, it renders the 'create_post.html'
    template.

    Returns:
    str: Rendered HTML content for 'create_post.html' template or redirects to
    the login page.
    """
    if request.method == "POST":
        # get user input and user details
        title = request.form['title']
        content = request.form['content']
        keywords = [tag.strip() for tag in request.form['keywords'].split(',') 
                    if tag.strip()]
        # verify title input
        if not title or len(title) > 50:
            flash("Title shall not be more than 50", "error")
            return render_template('create_post.html', title_input=title, 
                                   textarea_content=content)
        # verify content input
        if not content or len(content) > 1000:
            flash("Post content shall not be more than 1000", "error")
            return render_template('create_post.html', title_input=title, 
                                   textarea_content=content)

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
        return save_post(title, content, author, keywords, date_stamp)
        
    # if GET method check if user in session if not redirect to log in
    if "user" in session:
        return render_template("create_post.html")
    else:
        flash("Log in to post", "error")
        return redirect(url_for("login"))


# save post to mongoDB function
def save_post(title, content, author, keywords, date_stamp):
    """
    Save post to MongoDB function.

    This function takes the title, content, author details, keywords, and
    date stamp as input and inserts a new post into the MongoDB collection.

    Args:
    title (str): The title of the blog post.
    content (str): The content of the blog post.
    author (dict): Dictionary containing author details (id, username).
    keywords (list): List of keywords/tags associated with the blog post.
    date_stamp (str): Date stamp in the format '%d-%m-%Y %H:%M:%S'.

    Returns:
    str: Redirects to the 'get_posts' route after successfully saving the post.
    """
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


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        keywords = [tag.strip() for tag in request.form['keywords'].split(',') 
                    if tag.strip()]
        # verify title input
        if not title or len(title) > 50:
            flash("Title shall not be more than 50", "error")
            return render_template('create_post.html', title_input=title, 
                                textarea_content=content)
        # verify content input
        if not content or len(content) > 1000:
            flash("Post content shall not be more than 1000", "error")
            return render_template('create_post.html', title_input=title, 
                                textarea_content=content)
        # update database original post
        mongo.db.posts.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": {"title": title, "content": content, 
                      "keywords": keywords}})
        flash("Post updated", "success")
        return redirect(url_for("get_posts"))
    # get and check if post exists in database
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    if post is not None:
        return render_template("edit_post.html", post=post)
    else:
        return "Post not found", 404


@app.route("/delete_post/<post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    posts = list(mongo.db.posts.find())
    mongo.db.posts.delete_one({'_id': ObjectId(post_id)})
    return redirect(url_for('get_posts'))


@app.route("/get_register", methods=["GET", "POST"])
def get_register():
    """
    Route handling function for user registration.

    If the request method is POST, this function retrieves user input for
    the username and password, checks if the username already exists, and
    registers the user if it's a new username. The password is hashed using
    Flask-Bcrypt's 'generate_password_hash' function before storing it in the
    database.

    If the request method is GET, it renders the 'register.html' template.

    Returns:
    str: Rendered HTML content for 'register.html' template or redirects to
    the 'profile' route after successful registration.
    """
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
    """
    Route handling function for user login.

    If the request method is POST, this function retrieves user input for
    the username and password, checks if the username exists, and verifies
    the password using Flask-Bcrypt's 'check_password_hash' function. If the
    login is successful, it sets the user to the session cookie and redirects
    to the 'profile' route.

    If the request method is GET, it renders the 'login.html' template.

    Returns:
    str: Rendered HTML content for 'login.html' template or redirects to
    the 'profile' route after successful login.
    """
    if request.method == "POST":
        # Assign form inputs to new variables
        username = request.form.get('username').lower()
        password = request.form.get('password')

        user_id = mongo.db.users.find_one({'username': username})

        if user_id and check_password_hash(user_id['password'], password):
            flash('Login successful!', 'success')
            session["user"] = request.form.get("username").lower()
            return redirect(url_for("profile"))
        else:
            flash('Invalid username or password. Please try again.', 'error')
    return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
def profile():
    """
    Route handling function for user profile.

    Checks if the user is in the session. If the user is in the session,
    retrieves the user's ID from the MongoDB collection and renders the
    'profile.html' template with the capitalized username. If the user is
    not in the session, redirects to the 'login' route.

    Returns:
    str: Rendered HTML content for 'profile.html' template or redirects to
    the 'login' route.
    """
    if "user" in session:
        image_url = url_for('static', filename='images/post_default.jpg')
        user_id = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
        user_posts = list(mongo.db.posts.find({"author.username": user_id}))
        return render_template('profile.html', username=user_id.capitalize(), 
                               post=user_posts, image_url=image_url)

    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    """
    Route handling function for user logout.

    Clears the 'user' key from the session to log out the user and
    redirects to the 'login' route. Displays a success flash message.

    Returns:
    str: Redirects to the 'login' route after logging out.
    """
    session.pop('user', None)
    flash('You have logged out', 'success')
    
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)