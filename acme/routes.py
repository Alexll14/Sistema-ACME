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

@app.route('/usuario/<username>/excluir', methods=['GET', 'POST'])
@login_required
def remover_admin(username):
    admin = Admin.query.filter_by(username=username).first()
    database.session.delete(admin)
    database.session.commit()
    flash('Conta excluido com sucesso!', 'success')
    return redirect(url_for('estoque'))

@app.route('/usuario')
@login_required
def lista_usuario():
    admin = Admin.query.all()
    return render_template('lista_usuario.html', admin=admin)

@app.route('/historico')
@login_required
def historico():
    return render_template('historico.html')

@app.route('/admin/login', methods=['GET', 'POST'])
def login_admin():
    form = FormLoginAdmin()

    if form.validate_on_submit() and 'submit' in request.form:
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin is None:
            form.username.errors.append('Usuário inexistente!')

        if admin and bcrypt.check_password_hash(admin.senha, form.senha.data):
            login_user(admin, remember=form.lembrar_dados.data)
            flash('Login feito com sucesso!','success')
            par_next = request.args.get('next')
            if par_next:
                return redirect(par_next)
            else:
                return redirect(url_for('estoque'))
        else:
            form.senha.errors.append('Senha incorreta!')

    return render_template('loginAdmin.html', form=form)

@app.route('/admin/cadastrar', methods=['GET', 'POST'])
def cadastrar_admin():
    form = FormCadastrarAdmin()

    if form.validate_on_submit() and 'submit' in request.form:
        nome_duplicado = Admin.query.filter_by(username=form.username.data).first()
        if nome_duplicado or form.confirmar_senha.errors:
            form.username.errors.append('Usuário já cadastrado!')
        else:
            senha_bcrypt = bcrypt.generate_password_hash(form.senha.data)
            admin = Admin(username=form.username.data, senha=senha_bcrypt)
            database.session.add(admin)
            database.session.commit()
            flash('Usuário administrador criado com sucesso!', 'success')
            return redirect(url_for('estoque'))

    if type(form.confirmar_senha.errors) == list:
        form.confirmar_senha.errors.append('As senhas não coincidem!')
        form.senha.errors.append('As senhas não coincidem!')
        form.confirmar_senha.errors.pop(0)
        form.senha.errors.pop(0)

    return render_template('cadastrarAdmin.html', form=form)

@app.route('/sair')
@login_required
def sair():
    logout_user()
    flash('Log-out feito com sucesso!', 'success')
    return redirect(url_for('home'))