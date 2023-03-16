from flask import Flask, render_template, redirect, session, flash, abort, sessions
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm


app = Flask(__name__)
app.app_context().push() 


app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedbacks"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "helloworld"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


debug = DebugToolbarExtension(app)

connect_db(app)

@app.route("/")
def home():
    return redirect("/register")


@app.route("/register", methods = ["GET", "POST"])
def register_user():
    """Show a form that when submitted will register/create a user. """

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password)
        user.email = email
        user.first_name = first_name
        user.last_name = last_name

        db.session.add(user)
        db.session.commit()

        session["username"] = user.username

        # on successful login, redirect to secret page
        return redirect(f"/users/{user.username}")

    else:

        return render_template("register.html", form = form)

# @app.route("/secret")
# def secret_route():
#     return "You made it!"



@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, password)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect (f"/users/{user.username}")

        else:   
            form.username.errors = ["Bad name/password"]
   
      
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """Logout users!"""

    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>")
def show_user_info(username):
    """Shows a single user info"""

    if "username" not in session or username != session["username"]:
        flash("You must be logged in to view!")
        return redirect("/login")

    else:
        user = User.query.filter_by(username=username).first()
        return render_template("user.html", user = user)


@app.route("/users/<username>/delete", methods = ["POST"])
def remove_user(username):
    """Remove user nad redirect to login."""

    if "username" not in session or username != session["username"]:
        flash("You are not authorized!")
 

    else: 
        user = User.query.filter_by(username=username).first()

        db.session.delete(user)
        db.session.commit()

        return redirect("/")
    
    
    
@app.route("/users/<username>/feedback/add", methods = ["GET", "POST"])
def add_user_feedback(username):
    """Display a form to add feedback based on current user"""

    
    if "username" not in session or username != session["username"]:
        flash("Please login to view!")

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title = title, content = content, username = username)

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/users/{feedback.username}")

       
    else: 

        return render_template ("add_user_feedback.html", form = form)


@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("You are not authorized!")

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{feedback.username}")

    return render_template("/feedback/edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
                flash("You are not authorized!")


    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")
