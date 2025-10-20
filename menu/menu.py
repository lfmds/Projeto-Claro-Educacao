from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

tela1 = Blueprint('menu', __name__, template_folder='templates')

@tela1.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

@tela1.route('/')
def menu():
    return render_template('menu.html')
    #return 'menu'