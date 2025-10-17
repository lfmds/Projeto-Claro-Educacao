from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = "chave_teste"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickstart_app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# inicializa o banco de dados
db = SQLAlchemy(app)

# table user
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), nullable=False, default=True)

with app.app_context():
    db.create_all()

# configura flask login
login_manager = LoginManager()
login_manager.login_view = 'login' # rota para redirecionamento de login
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Rota Registro
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        check_password = request.form['check_password']

        # validações
        if password != check_password:
            flash("As senhas não conferem")
            return redirect(url_for('register'))
        
        if User.query.filter_by(username=username).first():
            flash("Usuario ja existe")
            return redirect(url_for('register'))
        
        if User.query.filter_by(email=email).first():
            flash("Usuario ja existe")
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Usuario criado com sucesso! Faça login")
        return redirect(url_for('login'))
    return render_template('register.html')

# Rota de Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuário ou senha inválidos!')
    return render_template('login.html')

# ROta Logout
@app.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Rota inicial
@app.route('/')
def home():
    return redirect(url_for('login'))

# Rota Protegida para Teste
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True, port=5152)
