# Show a form that when submitted will register/create a user. 
# This form should accept a username, password, email, first_name, and last_name.

# Make sure you are using WTForms and that your password input hides the characters
#  that the user is typing!

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired


class RegisterForm(FlaskForm):
    """Form for registering user"""

    username = StringField("Username", validators = [InputRequired()])
    password = PasswordField("Password", validators = [InputRequired()], render_kw={"type": "password"})
    email = StringField("Email", validators = [InputRequired()])
    first_name = StringField("First Name", validators = [InputRequired()])
    last_name = StringField("Last Name", validators = [InputRequired()])


class LoginForm(FlaskForm):
    """Form for logging a user."""

    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()], render_kw={"type": "password"})

class FeedbackForm(FlaskForm):
    """Form for adding user feedback"""

    title = StringField("Add Title", validators=[InputRequired()])
    content = StringField("Add Content", validators=[InputRequired()])

class DeleteForm(FlaskForm):
    """Delete form -- this form is intentionally blank."""
