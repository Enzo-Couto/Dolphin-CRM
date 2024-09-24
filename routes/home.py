from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user
from database.models.cliente import Users
from peewee import DoesNotExist

auth_route = Blueprint('auth', __name__)

@auth_route.route('/')
def login():
    return render_template('login.html')

@auth_route.route('/auth', methods=['POST'])
def auth():
    email = request.form['email']
    password = request.form['password']

    try:
        user = Users.get(Users.email == email)
        
        if user.password == password:
            login_user(user)
            return redirect(url_for('cliente.home'))
        else:
            flash('Credenciais inválidas. Tente novamente.')
            return redirect(url_for('auth.login'))
        
    except DoesNotExist:
        flash('Credenciais inválidas. Tente novamente.')
        return redirect(url_for('auth.login'))
