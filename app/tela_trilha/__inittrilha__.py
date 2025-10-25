from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import current_user, logout_user

trilha = Blueprint('trilha', __name__, template_folder='templates')

@trilha.before_request
def require_login():
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))

@trilha.route('/', methods=['GET', 'POST'])
def telatrilha():
    if request.method == "POST":
        if 'action' in request.form and request.form['action'] == 'logout':
            logout_user()
            return redirect(url_for('main.login'))
        elif 'action' in request.form and request.form['action'] == 'forum':
            return redirect(url_for('forum.forum_page'))
        elif 'action' in request.form and request.form['action'] == 'setsites':
            return redirect(url_for('setsites.set_sites_page'))
    return render_template('telatrilha.html')
        #return "trilha"


@trilha.route('/Português', methods=['GET', 'POST'])
def trilha1():
    if request.method == "POST":
        if 'action' in request.form and request.form['action'] == 'voltar':
            return redirect(url_for('trilha.telatrilha'))
    return render_template('trilha1.html')

@trilha.route('/Matemática', methods=['GET', 'POST'])
def trilha2():
    if request.method == "POST":
        if 'action' in request.form and request.form['action'] == 'voltar':
            return redirect(url_for('trilha.telatrilha'))
    return render_template('trilha2.html')


@trilha.route('/Ciências', methods=['GET', 'POST'])
def trilha3():
    if request.method == "POST":
        if 'action' in request.form and request.form['action'] == 'voltar':
            return redirect(url_for('trilha.telatrilha'))
    return render_template('trilha3.html')



