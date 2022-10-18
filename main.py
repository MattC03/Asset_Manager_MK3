import datetime
from functools import wraps
from flask import Flask, render_template, redirect, url_for, flash, abort
from sqlalchemy import ForeignKey, Column, String, Integer, Boolean, Text
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import forms
# import ldap3

##SETUP APP
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

##LDAP Connection


##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///asset_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##CONFIGURE TABLES

class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    name = Column(String(255), unique=True, nullable=True)
    password = Column(String(255), nullable=False)
    power_value = Column(Integer, nullable=False)
    change_password_needed = Column(Boolean)


class Asset(db.Model):
    id = Column(Integer, primary_key=True)
    asset_id = Column(String(250), nullable=False, unique=True)
    location = Column(String(250), nullable=False)
    department = Column(String(250), nullable=False)
    date_added = Column(String(250), nullable=False)
    serial_num = Column(String(250), nullable=False, unique=True)
    device = Column(String(250), nullable=False)
    make_and_model = Column(String(250), nullable=False)
    added_by = Column(String(250), nullable=False)
    imei = Column(String(250), nullable=True, unique=True)
    sim_number = Column(String(250), nullable=True, unique=True)
    notes = Column(Text, nullable=False)
    decommissioned = Column(Boolean, nullable=False)

db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.power_value != 1:
            return abort(403)
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    if current_user.is_authenticated:
        assets = Asset.query.all()
        return render_template("index.html", all_assets=assets)
    else:
        return redirect((url_for('login')))


@app.route('/register', methods=['GET', 'POST'])
# @login_required
# @admin_only
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        # Checks to see if there is a user with that email already.
        if db.session.query(User).filter_by(email=form.email.data).first():
            flash("Already an account with this email registered!")
            return render_template("register.html", form=form)

        # Creates a new user from the form.
        new_user = User()
        new_user.email = form.email.data
        new_user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user.name = form.name.data
        new_user.power_value = 0
        new_user.change_password_needed = True
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))

    return render_template("register.html", form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email=form.email.data).first()
        if user is not None:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                if user.change_password_needed:
                    return redirect(url_for("change_password"))
                return redirect(url_for('index'))
            else:
                flash("Incorrect password, please try again.")
                return redirect(url_for("login", form=form))
        else:
            flash("The email is not recognized please try again or create an account.")
            return redirect(url_for("login", form=form))
    return render_template("login.html", form=form)


@app.route('/change-password/', methods=['GET', 'POST'])
def change_password():
    form = forms.ChangePassword()
    if form.validate_on_submit():
        current_user.password = generate_password_hash(form.new_password.data, method='pbkdf2:sha256',
                                                       salt_length=8)
        current_user.change_password_needed = False
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("change-password.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

# #### ASSET MANAGEMENT #####

@app.route("/new-asset", methods=['GET', 'POST'])
@login_required
def new_asset():
    form = forms.CreateAssetForm()
    # On a valid submit of the form.
    if form.validate_on_submit():
        # Make sure asset id is not already used.
        if not db.session.query(Asset).filter_by(asset_id=form.asset_id.data).first():
            # Make sure that serial number is not already in there.
            if not db.session.query(Asset).filter_by(asset_id=form.serial_num.data).first():
                # Make the asset and submit it to the database.
                new_asset = Asset(
                    location=form.location.data,
                    department=form.department.data,
                    asset_id=form.asset_id.data,
                    date_added=datetime.date.today().strftime("%d/%m/%Y"),
                    serial_num=form.serial_num.data,
                    device=form.device.data,
                    make_and_model=form.make_and_model.data,
                    added_by=current_user.name,
                    notes=form.notes.data,
                    imei=form.imei.data,
                    sim_number=form.sim_number.data,
                    decommissioned=form.decommissioned.data,
                )
                db.session.add(new_asset)
                db.session.commit()
                flash(f"Asset {form.asset_id.data} has been added!")
                return redirect(url_for("index"))
            else:
                flash("This serial has already been used.")
                return render_template("new-asset.html", form=form)
        else:
            flash("This asset # has already been used.")
            return render_template("new-asset.html", form=form)
    return render_template("new-asset.html", form=form)


@app.route("/edit-asset/<int:asset_id>", methods=['GET', 'POST'])
@login_required
def edit_asset(asset_id):
    # Builds the form and find the asset in the database. Loads a different form if the user is an admin.
    if current_user.power_value == 1:
        form = forms.EditAssetFormAdmin()
    else:
        form = forms.EditAssetForm()
    asset_to_edit = db.session.query(Asset).filter_by(id=asset_id).first()

    # Checks to see if the form is submitted and then does the edit on database.
    if form.validate_on_submit():
        asset_to_edit.location = form.location.data
        asset_to_edit.department = form.department.data
        asset_to_edit.notes = form.notes.data
        asset_to_edit.sim_number = form.sim_number.data
        asset_to_edit.decommissioned = form.decommissioned.data
        asset_to_edit.added_by = current_user.name
        asset_to_edit.date_added = datetime.date.today().strftime("%d/%m/%Y")
        if current_user.power_value == 1:
            asset_to_edit.asset_id = form.asset_id.data
            asset_to_edit.serial_num = form.serial_num.data
            asset_to_edit.device = form.device.data
            asset_to_edit.make_and_model = form.make_and_model.data
            asset_to_edit.imei = form.imei.data
        db.session.commit()
        flash(f"Asset # {asset_to_edit.asset_id} has been updated!")
        return redirect(url_for("index"))

    # Pre-populates the form with the correct information. The form has the parts that should not be edited disabled.
    form.id.data = asset_id
    form.asset_id.data = asset_to_edit.asset_id
    form.serial_num.data = asset_to_edit.serial_num
    form.location.data = asset_to_edit.location
    form.department.data = asset_to_edit.department
    form.device.data = asset_to_edit.device
    form.make_and_model.default = asset_to_edit.make_and_model
    form.notes.data = asset_to_edit.notes
    form.imei.data = asset_to_edit.imei
    form.sim_number.data = asset_to_edit.sim_number
    form.decommissioned.data = asset_to_edit.decommissioned

    return render_template("edit-asset.html", form=form, asset_id=asset_id)


@app.route("/delete/<int:asset_id>")
@admin_only
def delete_asset(asset_id):
    asset_to_delete = db.session.query(Asset).filter_by(id=asset_id).first()
    db.session.delete(asset_to_delete)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
