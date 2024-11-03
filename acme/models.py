from acme import database, LoginManager, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_usuario(id):
    return Admin.query.get(int(id))

class Admin(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)

class Produto(database.Model):
    nome_produto = database.Column(database.String, nullable=False, unique=True)
    preco_produto = database.Column(database.Float, nullable=False)
    qtd_produto = database.Column(database.Integer, nullable=False)
    cat_produto = database.Column(database.String, default='sem categoria')
    foto_produto = database.Column(database.String, default='default.jpg')
    id_produto = database.Column(database.Integer, primary_key=True)