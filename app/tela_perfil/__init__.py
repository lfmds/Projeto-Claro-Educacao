from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user

perfil = Blueprint('perfil', __name__, template_folder='templates')

@perfil.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))  
    
@perfil.route('/perfil', methods=['GET', 'POST'])
def perfil_page():
    if request.method == "POST":
        if 'action' in request.form and request.form['action'] == 'back':
            return redirect(url_for('trilha.telatrilha'))
    return render_template('perfil.html')