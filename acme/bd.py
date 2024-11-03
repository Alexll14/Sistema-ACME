#arquivo para criar banco de dados, pode ser apagado posteriormente


from acme import app,database
from acme.models import Admin, Produto

with app.app_context():
    database.create_all()