from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

tela_trilha = Blueprint('tela_trilha', __name__, template_folder='templates')

@tela_trilha.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

@tela_trilha.route('/trilha')
def telatrilha():
    return render_template('telatrilha.html')
    #return "trilha"

