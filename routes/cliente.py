from flask import Flask, render_template, request, redirect, url_for, flash, Blueprint
from database.models.cliente import Cliente, Users
from peewee import DoesNotExist
from flask_login import login_user, logout_user, login_required, current_user

cliente_route = Blueprint('cliente', __name__)

@cliente_route.route('/home')
def home():
    return render_template('index.html')

@cliente_route.route('/')
def lista_clientes():
    clientes = Cliente.select()
    return render_template('lista_clientes.html', clientes=clientes)
    

@cliente_route.route('/', methods=['POST'])
def inserir_cliente():
    data = request.json
    
    novo_usuario = Cliente.create(
        nome = data['nome'],
        email = data['email'],
    )
    
    return render_template('item_cliente.html', cliente=novo_usuario)
    

@cliente_route.route('/new')
def form_cliente():
    return render_template('form_cliente.html')

@cliente_route.route('/<int:cliente_id>')
def detalhe_cliente(cliente_id):
    
    cliente = Cliente.get_by_id(cliente_id)
    
    return render_template('detalhe_cliente.html', cliente=cliente)
    
@cliente_route.route('/<int:cliente_id>/edit')
def form_edit_cliente(cliente_id):
    
    cliente = Cliente.get_by_id(cliente_id)
    
    return render_template('form_cliente.html', cliente=cliente)

@cliente_route.route('/<int:cliente_id>/update', methods=['PUT',])
def atualizar_cliente(cliente_id):
    cliente = None
    data = request.json
    
    cliente_editado = Cliente.get_by_id(cliente_id)
    cliente_editado.nome = data['nome']
    cliente_editado.email = data['email']
    cliente_editado.save()
            
    return render_template('item_cliente.html', cliente=cliente_editado)

@cliente_route.route('/<int:cliente_id>/delete', methods=['DELETE',])
def deletar_cliente(cliente_id):
    
    cliente = Cliente.get_by_id(cliente_id)
    cliente.delete_instance()
    return {'deleted': 'ok'}

@cliente_route.route('/register', methods=['POST', 'GET'])
def registrar_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("As senhas não correspondem. Tente novamente.")
            return redirect(url_for('cliente.registrar_cliente'))

        try:
            if Users.select().where(Users.email == email).exists():
                flash("E-mail já cadastrado. Tente novamente.")
                return redirect(url_for('cliente.registrar_cliente'))

            Users.create(
                nome=nome,
                email=email,
                password=password
            )
            flash("Usuário registado com sucesso!")
            return redirect(url_for('cliente.registrar_cliente'))

        except Exception as e:
            flash(f'Ocorreu um erro: {e}')
            return redirect(url_for('cliente.registrar_cliente'))

    return render_template("registrar_cliente.html")
