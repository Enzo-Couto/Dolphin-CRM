from peewee import Model, CharField, DateTimeField, BooleanField
from flask_login import UserMixin
from database.database import db
import datetime

class Cliente(Model):
    nome = CharField()
    email = CharField()
    data_registro = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

class Users(Model, UserMixin):
    nome = CharField()
    email = CharField(unique=True)
    password = CharField()
    active = BooleanField(default=True)

    @property
    def is_active(self):
        return self.active

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    class Meta:
        database = db
