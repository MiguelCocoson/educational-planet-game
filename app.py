# import dependencies
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.fields.simple import SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

# setup flask app
app = Flask(__name__)
# setup sqlalchemy db for the app
db = SQLAlchemy(app)
# setup sqlalchemy db file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.db'
# setup secret key for app
app.config['SECRET_KEY'] = 'DevelopeandoPlanetas'
# setup encryption for passwords
bcrypt = Bcrypt(app)

# create db model for users_table


class UserTable(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    # the length of the password is longer due to hashing
    password = db.Column(db.String(80), nullable=False)

# setup flask forms


class RegistrationForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Create account")

    # validate if user exists
    def user_validation(self, username):
        existing_username = UserTable.query.filter_by(
            username=username.data).first()
        if existing_username:
            raise ValidationError(
                "Username already in use, please pick a different one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(
        min=4, max=20)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=40)], render_kw={"placeholder": "Password"})

    submit = SubmitField("Login")


# setup login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return UserTable.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)

# set up routes


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    return render_template("planets.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = UserTable.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('game'))
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()

    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data)
        new_user = UserTable(username=form.username.data,
                             password=encrypted_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('registration.html', form=form)

    

@app.route("/results", methods=["POST"])
def results():
    req = request.form
    planet1 = req["planet1"]
    planet2 = req["planet2"]
    planet3 = req["planet3"]
    planet4 = req["planet4"]
    planet5 = req["planet5"]
    planet6 = req["planet6"]
    planet7 = req["planet7"]
    planet8 = req["planet8"]

    all_planets = [planet1, planet2, planet3, planet4, planet5, planet6, planet7, planet8]
    planets_list = ["mercury", "venus", "earth", "mars", "jupiter", "saturn", "uranus", "neptune"]

    return render_template("results.html", all_planets=all_planets, planets_list=planets_list)

