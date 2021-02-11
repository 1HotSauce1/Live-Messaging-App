from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User_profiles, Friendships
from werkzeug.security import generate_password_hash, check_password_hash
from . import database
from sqlalchemy import or_

views = Blueprint('views', __name__)

##### Root #####

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        person_to_add = request.form.get('friend_name')

        friend = User_profiles.query.filter_by(name=person_to_add).first()

        # Checking if there is an account with that username
        if friend:
            # Checking if you are friends already
            already_friend1 = Friendships.query.filter_by(user_id1=friend.user_id).first()
            already_friend2 = Friendships.query.filter_by(user_id2=friend.user_id).first()

            if not already_friend1 and not already_friend2:
                flash('You have added {} to your friends list!'.format(friend.name), category='success')
                friendship = Friendships(current_user.user_id, friend.user_id)
                database.session.add(friendship)
                database.session.commit()
            else:
                flash('You are already friends with {}.'.format(friend.name), category='error')
        else:
            flash('Can\'t find the username.', category='error')

    friends_list = []
    friends_query = database.session.query(Friendships).filter(or_(Friendships.user_id1 == current_user.user_id,
                                                                    Friendships.user_id2 == current_user.user_id))

    for friend in friends_query:
        if friend.user_id1 != current_user.user_id:
            friends_list.append(User_profiles.query.filter_by(user_id=friend.user_id1).first())
        else:
            friends_list.append(User_profiles.query.filter_by(user_id=friend.user_id2).first())

    return render_template('home.html', user=current_user, friends_list=friends_list)

##### Authentication views #####

@views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User_profiles.query.filter_by(name=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash('You have logged in!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Password is wrong, please double check.', category='error')
        else:
            flash('The username is not registered.', category='error')

    return render_template('login.html', user=current_user)

@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.login'))

@views.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if there is another account with that username
        user = User_profiles.query.filter_by(name=username).first()
        if user:
            flash('The username is taken.', category='error')
        else:
            if (len(password) < 6):
                flash('The password can\'t contain less than 6 characters.', category='error')
            else:
                flash('Account successfully created!', category='success')
            
                new_user = User_profiles(username, generate_password_hash(password, method='sha256'), email)
                database.session.add(new_user)
                database.session.commit()

                login_user(new_user, remember=True)
                return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)