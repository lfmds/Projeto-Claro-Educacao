from flask import Flask, render_template
from extensoes import db, login_manager

# Importa os Blueprints depois de criar app, para evitar loop
from login.pag_login import Login_blueprint
from tela_trilha.pag_trilha import tela_trilha
from Insercao_sites.InsercaoSites import IncluirSites
from tela5.quintatela import telacinco
from menu.menu import tela1

app = Flask(__name__)

app.config['SECRET_KEY'] = "chave_teste"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickstart_app.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa as extensões
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login.login'

# Registra os blueprints
app.register_blueprint(Login_blueprint)
app.register_blueprint(tela_trilha)
app.register_blueprint(IncluirSites)
app.register_blueprint(telacinco)
app.register_blueprint(tela1, url_prefix='/menu')

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'), port=5443, debug=True)
