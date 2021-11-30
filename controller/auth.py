from flask import Blueprint, redirect, render_template, flash, request, url_for
from flask_login import login_required, logout_user, current_user, login_user
from application import login_manager
from form.login import LoginForm
from form.sign_up import SignupForm
from model.user import User
from application import db

auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user is None:
            user = User(
                username=form.username.data
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('static_bp.get_images'))
        flash('A user already exists with that username.')

    return render_template('sign_up.html', form=form, title='Project Tag Sign Up page')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('static_bp.get_images'))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(password=form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('static_bp.get_images'))
        flash('Invalid username/password combination')
        return redirect(url_for('auth_bp.login'))

    return render_template('login.html', form=form, title='Project Tag Log In page')


@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth_bp.login'))


@auth_bp.route("/logout", methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))
