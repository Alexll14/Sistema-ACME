from enum import unique

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField
from wtforms.fields.numeric import IntegerField
from wtforms.fields.simple import HiddenField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
#from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,
# o validator de e-mail será usado caso seja feito o login para usuarios que não sejam admin


class FormCadastrarAdmin(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8,20)])
    confirmar_senha = PasswordField('Confirmação da senha', validators=[DataRequired(), EqualTo('senha')])
    submit = SubmitField('Criar conta')


class FormLoginAdmin(FlaskForm):
    username = StringField('Nome de usuário', validators=[DataRequired()])
    senha = PasswordField('Senha', validators=[DataRequired(), Length(8, 20)])
    lembrar_dados = BooleanField('Lembrar dados de acesso')
    submit = SubmitField('Fazer login')


class FormCadastrarProduto(FlaskForm):
    nome_produto = StringField('Cadastrar nome do produto')
    preco_produto = FloatField('Cadastrar preço do produto')
    qtd_produto = IntegerField('Cadastrar quantidade do produto')
    cat_produto = StringField('Cadastrar categoria do produto')
    foto_produto = FileField('Cadastrar foto do produto', validators=[FileAllowed(['jpg','jpeg','png','webp'])])
    submit = SubmitField('Cadastrar produto')


class FormEntrada(FlaskForm):
    id_produto = HiddenField()
    qtd_produto = IntegerField('+')
    submit = SubmitField('+')

class FormSaida(FlaskForm):
    id_produto = HiddenField()
    qtd_produto = IntegerField('-')
    submit = SubmitField('-')