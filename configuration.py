from routes.home import auth_route
from routes.cliente import cliente_route
from database.database import db
from database.models.cliente import Cliente, Users
from playhouse.shortcuts import model_to_dict
from werkzeug.security import generate_password_hash


def configure_all(app):
    configure_routes(app)
    configure_db()

def configure_routes(app):
    app.register_blueprint(auth_route)
    app.register_blueprint(cliente_route, url_prefix='/clientes')

def configure_db():
    db.connect()
    db.create_tables([Cliente])
    db.create_tables([Users])
    
    if not Users.select().where(Users.email == 'admin@admin.com').exists():
        Users.create(
            nome='Admin',
            email='admin@admin.com',
            password='admin123'
        )