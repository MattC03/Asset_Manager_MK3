from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, TextAreaField, BooleanField, HiddenField
from wtforms.validators import DataRequired, InputRequired, EqualTo


##WTForm
class CreateAssetForm(FlaskForm):
    asset_id = StringField("Asset Number", validators=[InputRequired()])
    serial_num = StringField("Serial Number", validators=[InputRequired()])
    location = StringField("Location", validators=[InputRequired()])
    department = StringField("Department")
    device = SelectField("Device Type", choices=[("Laptop", "Laptop"), ("Phone", "Phone"), ("Monitor", "Monitor")],
                         validators=[InputRequired()])
    make_and_model = StringField("Make & Model", validators=[InputRequired()])
    imei = StringField("IMEI Number")
    sim_number = StringField("String Number")
    notes = TextAreaField("Notes")
    decommissioned = BooleanField("Decommissioned")
    submit = SubmitField("Add Asset")

class ChangePassword(FlaskForm):
    new_password = PasswordField("New Password", validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('new_password')])
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
    location = StringField("Location", validators=[InputRequired()])
    department = StringField("Department")
    device = StringField("Device Type", render_kw={'readonly': True})
    make_and_model = StringField("Make & Model", render_kw={'readonly': True})
    imei = StringField("IMEI Number", render_kw={'readonly': True})
    sim_number = StringField("String Number")
    notes = TextAreaField("Notes")
    decommissioned = BooleanField("Decommissioned")
    submit = SubmitField("Edit Asset")


class EditAssetFormAdmin(FlaskForm):
    id = HiddenField("ID")
    asset_id = StringField("Asset Number")
    serial_num = StringField("Serial Number")
    location = StringField("Location")
    department = StringField("Department")
    assigned_to = SelectField("Assigned To")
    device = StringField("Device Type")
    make_and_model = StringField("Make & Model")
    imei = StringField("IMEI Number")
    sim_number = StringField("String Number")
    notes = TextAreaField("Notes")
    decommissioned = BooleanField("Decommissioned")
    submit = SubmitField("Edit Asset")
