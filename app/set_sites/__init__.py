from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user

setsites = Blueprint('setsites', __name__, template_folder='templates')

@setsites.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    
@setsites.route('/setsites', methods=['GET', 'POST'])
def set_sites_page():
    if request.method == "POST":
        if 'action' in request.form and request.form['action'] == 'back':
            return redirect(url_for('trilha.telatrilha'))
    return render_template('setsites.html')