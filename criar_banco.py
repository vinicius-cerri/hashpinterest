# Criar o Banco de Dados
from hashpinterest import database, app
from hashpinterest.models import Usuario, Foto

with app.app_context():
    database.create_all()