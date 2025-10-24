from flask import Flask
from .extensions import db, login_manager
from .auth import auth_bp
from .main import main_bp



def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "chave_teste"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quickstart_app.sqlite'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa as extensões
    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    

    # Registra os blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    # Cria as tabelas
    with app.app_context():
        db.create_all()

    return app