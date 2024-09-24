from flask import Flask
from flask_login import LoginManager
from configuration import configure_all
from database.models.cliente import Users
from peewee import DoesNotExist

app = Flask(__name__)
app.secret_key = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return Users.get(Users.id == user_id)
    except DoesNotExist:
        return None

configure_all(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
