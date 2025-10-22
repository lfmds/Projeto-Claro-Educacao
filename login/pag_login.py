from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from extensoes import db, login_manager  # Importa daqui agora
import re

regex_username = r"^[A-Za-z]{3,}$" #Restringe apenas letras, com limite mínimo de 3 caracteres
regex_email = r"^[a-zA-Z0-9._%+-]+@gmail\.com$" #Deve ser um e-mail válido com domínio @gmail.com
regex_senha = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9]).{8,}$" #Restringe senhas com limite de 8 caratacteres, incluindo maiúsculas, minúsculas e números

Login_blueprint = Blueprint('login', __name__, template_folder='templates')

# Modelo de usuário
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@Login_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('menu.menu'))
        else:
            flash('Usuário ou senha inválidos!')
    return render_template('login.html')

@Login_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        if 'action' in request.form and request.form['action'] == 'back':
            return redirect(url_for('login.login'))

        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        check_password = request.form['check_password']

        # Validação do Nome de Usuário 
        if not re.match(regex_username, username):
            flash("O nome de usuário deve conter mínimo 3 caracteres e apenas letras.")
            return redirect(url_for('login.register'))

        # Validação do E-mail 
        if not re.match(regex_email, email):
            flash("O e-mail deve ser válido e ter o domínio @gmail.com.")
            return redirect(url_for('login.register'))

        # Validação de Formato da Senha 
        if not re.match(regex_senha, password):
            flash("Senhas com limite de 8 caracteres, incluindo maiúsculas, minúsculas e números")
            return redirect(url_for('login.register'))

        #Confirmação de Senha
        if password != check_password:
            flash("As senhas não conferem.")
            return redirect(url_for('login.register'))

        # Resto das checagens de usuário e e-mail existente no DB
        if User.query.filter_by(username=username).first():
            flash("Usuário já existe")
            return redirect(url_for('login.register'))
        
        if User.query.filter_by(email=email).first():
            flash("E-mail já cadastrado")
            return redirect(url_for('login.register'))
        
        #Criação e salvamento do novo usuário
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Usuário criado com sucesso! Faça login.")
            return redirect(url_for('login.login'))
        except Exception as e:
            db.session.rollback()
            flash("Erro ao salvar no banco. Tente novamente mais tarde.")
            print(f"[ERRO DB] {e}") 
            return redirect(url_for('login.register'))
    return render_template('register.html')

@Login_blueprint.before_request
def restringir_login():
    if current_user.is_authenticated and request.endpoint in ['login.login', 'login.register']:
        return redirect(url_for('menu.menu'))
