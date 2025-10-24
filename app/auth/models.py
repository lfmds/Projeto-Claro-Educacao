from ..extensions import db, login_manager
from flask_login import UserMixin

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
