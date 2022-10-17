from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField, BooleanField, HiddenField
from wtforms.validators import DataRequired, URL, InputRequired, EqualTo


##WTForm
class CreateAssetForm(FlaskForm):
    asset_id = StringField("Asset Number", validators=[InputRequired()])
    serial_num = StringField("Serial Number", validators=[InputRequired()])
    assigned_to = SelectField("Assigned To", validators=[InputRequired()])
    device = SelectField("Device Type", choices=[("Laptop", "Laptop"), ("Phone", "Phone"), ("Monitor", "Monitor")],
                         validators=[InputRequired()])
    product = StringField("Make & Model", validators=[InputRequired()])
    notes = TextAreaField("Notes")
    decommissioned = BooleanField("Decommissioned")
    submit = SubmitField("Add Asset")


class CreateUserForm(FlaskForm):
    firstname = StringField("First Name", validators=[InputRequired()])
    lastname = StringField("Last Name", validators=[InputRequired()])
    department = StringField("Department", validators=[InputRequired()])
    submit = SubmitField("Add User")


class ChangePassword(FlaskForm):
    new_password = PasswordField("New Password", validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired()])
    submit = SubmitField("Change Password")


class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    name = StringField("Name", validators=[InputRequired()])
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")


class EditAssetForm(FlaskForm):
    id = HiddenField("ID")
    asset_id = StringField("Asset Number", render_kw={'readonly': True})
    serial_num = StringField("Serial Number", render_kw={'readonly': True})
    assigned_to = SelectField("Assigned To", validators=[InputRequired()])
    device = StringField("Device Type", render_kw={'readonly': True})
    product = StringField("Make & Model", render_kw={'readonly': True})
    notes = TextAreaField("Notes")
    decommissioned = BooleanField("Decommissioned")
    submit = SubmitField("Edit Asset")


class EditAssetFormAdmin(FlaskForm):
    id = HiddenField("ID")
    asset_id = StringField("Asset Number")
    serial_num = StringField("Serial Number")
    assigned_to = SelectField("Assigned To")
    device = StringField("Device Type")
    product = StringField("Make & Model")
    notes = TextAreaField("Notes")
    decommissioned = BooleanField("Decommissioned")
    submit = SubmitField("Edit Asset")
