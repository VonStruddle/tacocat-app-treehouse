from flask import Flask, g, render_template, flash, redirect, url_for
from flask.ext.bcrypt import check_password_hash
from flask.ext.login import LoginManager, login_user, logout_user, login_required, current_user

import forms
import models


DEBUG = True
PORT = 8080
HOST = '0.0.0.0'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    try:
        return models.User.get(models.User.id == user_id)
    except:
        return None


@app.before_request
def before_request():
    g.db = models.DB
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    tacos = models.Taco.select()
    return render_template('index.html', tacos=tacos)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("You've successfully logged in!")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've successfully logged out!")
    return redirect(url_for('index'))


if __name__ == '__main__':
    models.initializeDB()
    try:
        models.User.create_user(
            email='quentin.durantay@gmail.com'
            password='passwordsohard'
        )
        models.User.create_user(
            email='quentin.durantay@outlook.com'
            password='passwordsohard2'
        )
    except ValueError:
        pass
    app.run(host=HOST, port=PORT, debug=DEBUG)
