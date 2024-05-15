from . import auth
from flask import render_template, redirect, url_for, request, flash, session, jsonify
from .forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from app import db
from werkzeug.security import check_password_hash
    
# TAMAMLANDI.
@auth.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'}), 400
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Kullanıcıyı veritabanından al
    user = User.query.filter_by(username=username).first()

    # Kullanıcı varsa ve şifre doğruysa
    if user and verify_password(user.password_hash, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'message': 'Invalid username or password'}), 401

def verify_password(hashed_password, input_password):
    return check_password_hash(hashed_password, input_password)

# TAMAMLANDI.
# Çıkış endpoint'i
@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200 
  
# TAMAMLANDI.  
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'Missing username, email, or password'}), 400

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'message': 'Username is already taken'}), 400

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'message': 'Email is already registered'}), 400

    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201

# TAMAMLANDI.
@auth.route('/user_info')
def user_info():
    if current_user.is_authenticated:
        return jsonify({'isAuthenticated': True, 'username': current_user.username})
    else:
        return jsonify({'isAuthenticated': False})