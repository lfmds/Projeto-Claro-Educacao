from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user, logout_user
from flask_login import current_user

perfil = Blueprint('perfil', __name__, template_folder='templates', static_folder='static', static_url_path='/perfil/static')

@perfil.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))  
    
@perfil.route('/perfil', methods=['GET', 'POST'])
def perfil_page():
    if request.method == "POST":
        # Esta é a lógica que será acionada pelo formulário/botão no HTML
        if 'action' in request.form and request.form['action'] == 'logout':
            logout_user()
            return redirect(url_for('main.login'))
        
    # Se a requisição for GET, ou se não for um logout, renderiza a página
    return render_template('perfil.html', user=current_user) # Certifique-se de que o render_template está aqui