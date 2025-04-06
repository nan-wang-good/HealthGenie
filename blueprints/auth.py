from flask import render_template, request, redirect, url_for, flash, session, jsonify
from . import auth_bp
from models.user import User
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from db import db
import re

# check if user exists（by checking email in SQLite)
def user_exists(email):
    user = User.query.filter_by(email=email).first()
    return user is not None

# Check whether the password meets the strength requirements
def is_valid_password(password):
    # Regular expression check: at least 8 characters, including at least one uppercase letter, one lowercase letter, one number, and one special character
    pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_])[A-Za-z\d\W_]{8,}$')
    return bool(pattern.match(password))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        errors = {}

        if not user or not check_password_hash(user.pwd, password):
            return jsonify({'success': False, 'errors': {'email': 'Invalid email or password'}})

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            session['user_email'] = user.email
            session['nickname'] = user.nickname
            return jsonify({'success': True, 'redirect': url_for('index')})

        session['user_email'] = user.email
        session['nickname'] = user.nickname
        return redirect(url_for('index'))

    return render_template('auth/login.html', active_tab='login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        email = request.form.get('email')
        password = request.form.get('password')
        print(password)

        if user_exists(email):
            return jsonify({'success': False, 'errors': {'email': 'This email is already registered'}})

        # Check that the password meets the requirements
        if not is_valid_password(password):
            return jsonify({'success': False, 'errors': {'password': "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character."}})

        try:
            new_user = User(email=email, nickname=nickname, password=password)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'success': True, 'redirect': url_for('auth.login')})
        except Exception:
            db.session.rollback()
            return jsonify({'success': False, 'errors': {'email': 'Registration failed, please try again'}})
    return render_template('auth/login.html', active_tab='register')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')

        if not user_exists(email):
            flash('Email not registered', 'error')
            return redirect(url_for('auth.forgot_password'))

        return redirect(url_for('auth.reset_password', email=email))

    return render_template('auth/forgot_password.html')

@auth_bp.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    email = request.args.get('email')
    if not email or not user_exists(email):
        flash('Invalid email', 'error')
        return redirect(url_for('auth.forgot_password'))

    if request.method == 'POST':
        password = request.form.get('password')
        if not password:
            return jsonify({'success': False, 'errors': {'password': 'Please enter new password'}})

        if not is_valid_password(password):
            return jsonify({'success': False, 'errors': {'password': "Password must be at least 8 characters long, contain at least one uppercase letter, one lowercase letter, one number, and one special character."}})

        user = User.query.filter_by(email=email).first()
        user.pwd = generate_password_hash(password)  # Ensure hashed value
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Password reset successful! Please login with your new password',
            'redirect': url_for('auth.login')
        })

    return render_template('auth/reset_password.html', email=email)
