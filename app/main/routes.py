
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re
from . import main_bp
from .models import User
from ..extensions import db



regex_username = r"^[A-Za-z]{3,}$" #Restringe apenas letras, com limite mínimo de 3 caracteres
regex_email = r"^[a-zA-Z0-9._%+-]+@gmail\.com$" #Deve ser um e-mail válido com domínio @gmail.com
regex_senha = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$" #Restringe senhas com limite de 8 caratacteres, incluindo maiúsculas, minúsculas e números


@main_bp.route('/', methods=['GET', 'POST'])
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
        else:
            flash('Usuário ou senha inválidos!')
    return render_template('index.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if 'action' in request.form and request.form['action'] == 'back':
            return redirect(url_for('main.login'))

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        check_password = request.form['check_password']

        # Validação do Nome de Usuário 
        if not re.match(regex_username, username):
            flash("O nome de usuário deve conter mínimo 3 caracteres e apenas letras.")
            return redirect(url_for('main.register'))

        # Validação do E-mail 
        if not re.match(regex_email, email):
            flash("O e-mail deve ser válido e ter o domínio @gmail.com.")
            return redirect(url_for('main.register'))

        # Validação de Formato da Senha 
        if not re.match(regex_senha, password):
            flash("Senhas com limite de 8 caracteres, incluindo maiúsculas, minúsculas e números")
            return redirect(url_for('main.register'))

        #Confirmação de Senha
        if password != check_password:
            flash("As senhas não conferem.")
            return redirect(url_for('main.register'))

        # Resto das checagens de usuário e e-mail existente no DB
        if User.query.filter_by(username=username).first():
            flash("Usuário já existe")
            return redirect(url_for('main.register'))
        
        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado")
            return redirect(url_for('main.register'))

        #Criação e salvamento do novo usuário
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Usuário criado com sucesso! Faça login.")
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao salvar no banco. Tente novamente mais tarde.")
            print(f"[ERRO DB] {e}")
            return redirect(url_for('main.register'))
    return render_template('register.html')

