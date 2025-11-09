
from flask import render_template, redirect, url_for, request
from flask_login import login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import main_bp
from .models import User
from ..extensions import db


@main_bp.route('/')
def menu():
    return render_template('index.html')

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('trilha.telatrilha'))

    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('trilha.telatrilha'))
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if 'action' in request.form and request.form['action'] == 'back':
            return redirect(url_for('main.login'))

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        check_password = request.form['check_password']

        #Confirmação de Senha
        if password != check_password:
            return redirect(url_for('main.register'))

        # Resto das checagens de usuário e e-mail existente no DB
        if User.query.filter_by(username=username).first():
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(email=email).first():
            return redirect(url_for('main.register'))

        #Criação e salvamento do novo usuário
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            print(f"[ERRO DB] {e}")
            return redirect(url_for('main.register'))
    return render_template('register.html')

