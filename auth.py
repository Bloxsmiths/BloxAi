# auth.py
from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import json, os

auth_bp = Blueprint('auth', __name__)
USER_FILE = 'users.json'

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        # Pastikan username ada dan verifikasi hash
        if username in users and check_password_hash(users[username], password):
          session.permanent = False  # <--- tambahkan ini
          session['username'] = username
          return redirect(url_for('home'))
        else:
            return render_template('login.html', error="Username atau password salah!")
    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if not username or not password:
            return render_template('register.html', error="Username dan password tidak boleh kosong.")

        if username in users:
            return render_template('register.html', error="Username sudah digunakan.")

        # Simpan password yang telah di-hash
        users[username] = generate_password_hash(password)
        save_users(users)
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))
