from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

IncluirSites = Blueprint('Insercao_sites', __name__, template_folder='templates') 

@IncluirSites.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('login.login'))

@IncluirSites.route('/setsite')
def incluir_site():
    return render_template('setsites.html')
    #return 'incluir sites'


