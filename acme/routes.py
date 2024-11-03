from acme import app, bcrypt, database
from acme.models import Admin, Produto
from acme.forms import FormLoginAdmin, FormCadastrarAdmin

from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, login_required, logout_user


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/estoque')
@login_required
def estoque():
    return render_template('estoque.html')

@app.route('/usuario')
@login_required
def lista_usuario():
    return render_template('lista_usuario.html')

@app.route('/historico')
@login_required
def historico():
    return render_template('historico.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    form = FormLoginAdmin()

    if form.validate_on_submit() and 'submit' in request.form:
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and bcrypt.check_password_hash(admin.senha, form.senha.data):
            login_user(admin, remember=form.lembrar_dados.data)
            flash('Login feito com sucesso!','success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('estoque'))

    return render_template('loginAdmin.html', form=form)

@app.route('/admin/cadastrar', methods=['GET', 'POST'])
def cadastrar_admin():
    form = FormCadastrarAdmin()

    if form.validate_on_submit() and 'submit' in request.form:
        senha_bcrypt = bcrypt.generate_password_hash(form.senha.data)
        admin = Admin(username=form.username.data, senha=senha_bcrypt)
        database.session.add(admin)
        database.session.commit()
        flash('Usuário administrador criado com sucesso!' , 'success')
        return redirect(url_for('login_admin'))

    return render_template('cadastrarAdmin.html', form=form)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Log-out feito com sucesso!', 'success')
    return redirect(url_for('home'))