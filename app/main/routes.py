from flask import render_template, redirect, url_for
from flask_login import current_user, login_required
from . import main_bp

@main_bp.route('/')
def home():
    """Página inicial (rota raiz: http://127.0.0.1:5000/)"""
    if current_user.is_authenticated:
        # se o usuário já estiver logado, manda pro dashboard
        return redirect(url_for('main.dashboard'))
    return render_template('main/index.html')  # carrega o template da página inicial

@main_bp.route('/dashboard')
@login_required
def dashboard():
    print(current_user.is_authenticated)
    return render_template('main/dashboard.html', user=current_user)