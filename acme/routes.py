from acme import app, bcrypt, database
from acme.models import Admin, Produto
from acme.forms import FormLoginAdmin, FormCadastrarAdmin, FormCadastrarProduto, FormEntrada, FormSaida

from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, login_required, logout_user

import secrets
import os
from PIL import Image

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/estoque')
@login_required
def estoque():
    produtos = Produto.query.all()
    formE = FormEntrada()
    formS = FormSaida()
    return render_template('estoque.html', produtos=produtos, formE=formE , formS=formS)

@app.route('/estoque/entrada', methods=['GET', 'POST'])
@login_required
def entrada():
    form = FormEntrada()
    id_produto = int(form.id_produto.data)
    produto = Produto.query.filter_by(id_produto=id_produto).first()
    produto.qtd_produto += form.qtd_produto.data
    database.session.commit()

    flash('Produto alterado com sucesso!', 'success')
    return redirect(url_for('estoque'))

@app.route('/estoque/saida', methods=['GET', 'POST'])
@login_required
def saida():
    form = FormSaida()
    id_produto = int(form.id_produto.data)
    produto = Produto.query.filter_by(id_produto=id_produto).first()
    produto.qtd_produto -= form.qtd_produto.data
    database.session.commit()

    flash('Produto alterado com sucesso!', 'success')
    return redirect(url_for('estoque'))

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

def salvar_imagem(imagem):
    codigo = secrets.token_hex(8)
    nome, extensao = os.path.splitext(imagem.filename)
    nome_arquivo = nome + codigo + extensao

    caminho_base = r'C:\Users\alexl\Documents\GitHub\pythonCrud\acme\static\fotos_produto'

    if not os.path.exists(caminho_base):
        os.makedirs(caminho_base)

    caminho_completo = os.path.join(caminho_base, nome_arquivo)

    tamanho = (400, 400)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    imagem_reduzida.save(caminho_completo)
    return nome_arquivo


@app.route('/cadastra_produto', methods=['GET', 'POST'])
@login_required
def cadastrar_produto():
    form = FormCadastrarProduto()

    if form.validate_on_submit():

        preco = form.preco_produto.data
        qtd = form.qtd_produto.data

        print(type(preco))

        if int(preco) <= 0:
            form.preco_produto.errors.append('Valor inválido, o valor precisa ser maior que zero!')
        elif int(qtd) <= 0:
            form.qtd_produto.errors.append('Valor inválido, o valor precisa ser maior que zero!')
        else:
            if form.foto_produto.data:
                nome_imagem = salvar_imagem(form.foto_produto.data)
                form.foto_produto = nome_imagem
            else:
                nome_imagem = 'default.jpg'
                form.foto_produto = nome_imagem

            produto = Produto(nome_produto=form.nome_produto.data, qtd_produto=form.qtd_produto.data, preco_produto=form.preco_produto.data, cat_produto=form.cat_produto.data, foto_produto=form.foto_produto)
            database.session.add(produto)
            database.session.commit()

            foto_produto = url_for('static', filename='fotos_produto/{}'.format(produto.foto_produto))

            flash('Produto inserido com sucesso!', 'success')
            return redirect(url_for('estoque'))

    if type(form.preco_produto.errors) == list:
        form.preco_produto.errors.append('Valor inválido!')
        form.preco_produto.errors.pop(0)
    if type(form.qtd_produto.errors) == list:
        form.qtd_produto.errors.append('Valor inválido!')
        form.qtd_produto.errors.pop(0)

    return render_template('cadastrarProduto.html', form=form)

@app.route('/estoque/excluir/<int:id_produto>', methods=['GET', 'POST'])
@login_required
def remover_produto(id_produto):
    produto = Produto.query.filter_by(id_produto=id_produto).first()
    deletar_imagem(produto.foto_produto)
    database.session.delete(produto)
    database.session.commit()
    flash('Produto excluido com sucesso!', 'success')
    return redirect(url_for('estoque'))

def deletar_imagem(imagem):

    caminho_base = r'C:\Users\alexl\Documents\GitHub\pythonCrud\acme\static\fotos_produto'

    caminho_completo = os.path.join(caminho_base, imagem)
    if os.path.exists(caminho_completo):
        os.remove(caminho_completo)