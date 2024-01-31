import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for, abort)
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
    Route handling function for the home page.

    Constructs the URL for a static image and renders the 'index.html'
    template, passing the image URL.

    Returns:
    str: Rendered HTML content for the 'index.html' template.
    """
    img_url = url_for("static", filename="images/cover.jpg")
    return render_template("index.html", img_url=img_url)


@app.route("/url_redirect/<template>", methods=["GET", "POST"])
def url_redirect(template):
    """
    Route handling function for URL redirection.

    This function redirects users based on the specified template parameter.

    Args:
    template (str): The template parameter determining the redirection
    behavior.

    Returns:
    Union[str, Response]: If template is "blog" and user is logged in,
    renders 'create_post.html'. If user is not logged in, flashes an error
    message, saves the current URL in the session, and redirects to the login
    page.

    Raises:
    500 Error: If an unsupported template is provided, raises a 500 error.
    """
    if template == "blog":
        if "user" in session:
            return render_template("create_post.html")
        else:
            flash("Log in to post", "error")
            session["blog_url"] = request.url
            return redirect(url_for("login"))
    else:
        abort(500)


@app.route("/url_edit/<post_id>/<template>", methods=["GET", "POST"])
def url_edit(post_id, template):
    """
    Route handling function for editing URLs.

    This function redirects users based on the specified template parameter.

    Parameters:
    post_id (str): The identifier of the post to be edited.
    template (str): The template parameter determining the editing behavior.

    Returns:
    Response: Redirects to the appropriate route based on the template.

    Raises:
    HTTPException: If an unsupported template is provided, raises a 500 error.
    """
    if template == "edit_profile":
        session["edit_profile"] = request.url
        return redirect(url_for("edit_post", post_id=post_id))
    else:
        abort(500)


@app.route("/url_delete/<post_id>/<template>", methods=["GET", "POST"])
def url_delete(post_id, template):
    """
    Route handling function for deleting URLs.

    This function redirects users based on the specified template parameter.

    Parameters:
    post_id (str): The identifier of the post to be deleted.
    template (str): The template parameter determining the deletion behavior.

    Returns:
    Response: Redirects to the appropriate route based on the template.

    Raises:
    HTTPException: If an unsupported template is provided, raises a 500 error.
    """
    if template == "delete_profile":
        session["delete_profile"] = request.url
        return redirect(url_for("delete_post", post_id=post_id))
    else:
        abort(500)


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
    post = list(mongo.db.posts.find())
    image_url = url_for("static", filename="images/post_default.jpg")
    return render_template("blog.html", post=post, image_url=image_url)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Route handling function for searching posts.

    Retrieves posts from the MongoDB database based on the provided search
    query.
    Renders the 'blog.html' template, passing the retrieved posts and a static
    image URL.

    Returns:
    str: Rendered HTML content for the 'blog.html' template.

    Raises:
    Any exceptions that may occur during template rendering or database query.
    """
    query = request.form.get("query")
    get_posts = list(mongo.db.posts.find({"$text": {"$search": query}}))
    image_url = url_for("static", filename="images/post_default.jpg")
    return render_template("blog.html", post=get_posts, image_url=image_url)


@app.route("/create_post", methods=["GET", "POST"])
def create_post():
    """
    Route handling function for creating a new post.

    If the request method is POST, retrieves user input and details, verifies
    the input for title and content, retrieves user details, and then calls
    the 'save_post' function to save the post. If the request method is GET,
    renders the 'create_post.html' template.

    Returns:
    Union[str, Response]: If the request method is POST and the post is
    successfully
    saved, redirects to a relevant page. If the request method is GET, renders
    the 'create_post.html' template.

    Raises:
    Any exceptions that may occur during the post creation process.
    """
    if request.method == "POST":
        # get user input and user details
        title = request.form["title"]
        content = request.form["content"]
        keywords = [tag.strip() for tag in request.form["keywords"].split(",")
                    if tag.strip()]
        # verify title input
        if not title or len(title) > 50:
            flash("Title shall not be more than 50", "error")
            return render_template("create_post.html", title_input=title,
                                   textarea_content=content)
        # verify content input
        if not content or len(content) > 1000:
            flash("Post content shall not be more than 1000", "error")
            return render_template("create_post.html", title_input=title,
                                   textarea_content=content)
        # get user details
        user_details = mongo.db.users.find_one({"username": session["user"]})
        # assign user details to author
        author = {
            "id": str(user_details["_id"]),
            "username": user_details["username"]
        }
        # create a date stamp with a specific format
        date_stamp = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")
        return save_post(title, content, author, keywords, date_stamp)
    return render_template("create_post.html")


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

    Raises:
    Any exceptions that may occur during the post creation process.
    """
    post_data = {
        "title": title,
        "content": content,
        "author": author,
        "keywords": keywords,
        "created_at": date_stamp
    }
    # insert the post into the MongoDB collection
    mongo.db.posts.insert_one(post_data)
    flash("Blog has been posted", "success")
    return redirect(url_for("get_posts"))


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    """
    Route handling function for editing a post.

    If the request method is POST, retrieves user input, verifies the input for
    title and content, and updates the original post in the database. If the
    request method is GET, retrieves the post from the database and renders the
    'edit_post.html' template.

    Parameters:
    post_id (str): The identifier of the post to be edited.

    Returns:
    Union[str, Response]: If the request method is POST and the post is
    successfully
    updated, redirects to a relevant page. If the request method is GET,
    renders
    the 'edit_post.html' template with the retrieved post.

    Raises:
    HTTPException: If the post with the specified post_id is not found, returns
    a 404 error.
    """
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        keywords = [tag.strip() for tag in request.form["keywords"].split(",")
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
        # redirection use check
        edit_profile = session.pop("edit_profile", None)
        if edit_profile:
            return redirect(url_for("profile"))
        return redirect(url_for("get_posts"))
    # get and check if post exists in database
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    if post is not None:
        return render_template("edit_post.html", post=post)
    else:
        abort(404)


@app.route("/delete_post/<post_id>", methods=["GET", "POST"])
def delete_post(post_id):
    """
    Route handling function for deleting a post.

    Gets and checks if the post with the specified post_id exists in the
    database.
    If found, deletes the post from the database. If the request method is
    POST,
    it then redirects to a relevant page based on the context.

    Parameters:
    post_id (str): The identifier of the post to be deleted.

    Returns:
    Union[str, Response]: If the post is successfully deleted, redirects to a
    relevant page based on the context.

    Raises:
    HTTPException: If the post with the specified post_id is not found, returns
    a 404 error.
    """
    # get and check if post exists in database
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    if post is not None:
        print(post)
        mongo.db.posts.delete_one(post)
        flash("Post deleted", "success")
        delete_profile = session.pop("delete_profile", None)
        if delete_profile:
            return redirect(url_for("profile"))
        return redirect(url_for("get_posts"))
    else:
        return "Post not found", 404


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

    Raises:
    Any exceptions that may occur during the post creation process.
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

    If the request method is POST, validates the entered username and password
    against the database. If successful, flashes a success message, creates a
    user session, and redirects based on any existing redirection session.
    If the request method is GET, renders the 'login.html' template.

    Returns:
    Union[str, Response]: If the login is successful and a redirection session
    exists, redirects to the relevant page. If the login is successful without
    a redirection session, redirects to the profile page. If the login is
    unsuccessful,
    renders the 'login.html' template.

    Raises:
    Any exceptions that may occur during the login process.
    """
    if request.method == "POST":
        # Assign form inputs to new variables
        username = request.form.get("username").lower()
        password = request.form.get("password")

        user = mongo.db.users.find_one({'username': username})
        # check if entered details match database
        if user and check_password_hash(user['password'], password):
            flash("Login successful!", "success")
            # create user session
            session["user"] = user['username']
            # check if url redirection session exists
            blog_url = session.pop("blog_url", None)
            # redirect base on the url session
            if blog_url:
                return redirect(url_for("create_post"))
            return redirect(url_for("profile"))
        else:
            flash("Invalid username or password. Please try again.", "error")
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

    Raises:
    Any exceptions that may occur during the login process.
    """
    user_id = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    if user_id:
        image_url = url_for('static', filename='images/post_default.jpg')
        user_posts = list(mongo.db.posts.find({"author.username": user_id}))
        return render_template('profile.html', username=user_id.capitalize(),
                               post=user_posts, image_url=image_url)
    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    """
    Route handling function for user logout.

    Logs out the user by clearing all items from the session, flashes a success
    message, and redirects to the login page.

    Returns:
    Response: Redirects to the login page after logging out.

    Raises:
    Any exceptions that may occur during the logout process.
    """
    for key in list(session.keys()):
        session.pop(key, None)
    flash('You have logged out', 'success')
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    """
    Error handler for 404 - Page Not Found.

    Renders the '404.html' template with a 404 status code.

    Parameters:
    error (Exception): The exception associated with the 404 error.

    Returns:
    Tuple[str, int]: Rendered HTML content for the '404.html' template and
    a 404 status code.
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Error handler for 500 - Internal Server Error.

    Renders the '500.html' template with a 500 status code.

    Parameters:
    error (Exception): The exception associated with the 500 error.

    Returns:
    Tuple[str, int]: Rendered HTML content for the '500.html' template and
    a 500 status code.
    """
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
