from flask import Flask, app
from .extensions import db, login_manager
from .main import main_bp
from .tela_trilha.__inittrilha__ import trilha
from .tela_forum.__initforum__ import forum   
from .set_sites import setsites
from .tela_perfil import perfil


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "chave_teste"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickstart_app.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa as extensões
    db.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)
    

    # Registra os blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(trilha, url_prefix='/trilha')
    app.register_blueprint(forum)
    app.register_blueprint(setsites)
    app.register_blueprint(perfil)
    
    # Cria as tabelas
    with app.app_context():
        db.create_all()

    return app