from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

telacinco = Blueprint('tela5', __name__, template_folder='templates') 

@telacinco.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

@telacinco.route('/tela5')
def tela_5():
    return render_template('tela5.html')
    #return 'tela 5'