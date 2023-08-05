# Criar as Rotas/Links do Site
from flask import render_template, url_for, redirect
from hashpinterest import app, database, bcrypt
from flask_login import login_required, login_user, logout_user, current_user
from hashpinterest.forms import FormLogin, FormCriarConta, FormFoto
from hashpinterest.models import Usuario, Foto
import os
from werkzeug.utils import secure_filename
# render_template -> É uma biblioteca que vai procurar uma pasta chamada templates e carregar os arquivos
# url_for -> É uma biblioteca que permite direcionar para um link específico usando o nome da função

# Página Principal do Site (Fazer Login)
@app.route("/", methods = ["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        usuario = Usuario.query.filter_by(email = form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template("homepage.html", form = form_login)

# Página de Criar Conta
@app.route("/criarconta", methods = ["GET", "POST"])
def criarconta():
    form_criarconta = FormCriarConta()
    if form_criarconta.validate_on_submit():
        # Criar o usuário no Banco de Dados
        senha = bcrypt.generate_password_hash(form_criarconta.senha.data) # Criptografa a senha do usuario, para ficar salva com segurança no banco de dados
        usuario = Usuario(username = form_criarconta.username.data, email = form_criarconta.email.data, senha = senha)
        database.session.add(usuario)
        database.session.commit()
        # Logar o usuário
        login_user(usuario, remember = True)
        # Redirecionar para Página de Perfil
        return redirect(url_for("perfil", id_usuario = usuario.id))
    return render_template("criarconta.html", form = form_criarconta)

# Página de Perfil
@app.route("/perfil/<id_usuario>", methods = ["GET", "POST"])
@login_required
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id):
        # Visualizar o próprio perfil
        form_foto = FormFoto()
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)
            # Salvar o arquivo na pasta fotos_posts
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), app.config["UPLOAD_FOLDER"], nome_seguro)
            # os.path.abspath(os.path.dirname(__file__)) --> caminho do próprio arquivo, no caso o caminho do arquivo "routes"
            arquivo.save(caminho)
            # Registrar esse arquivo no Banco de Dados
            foto = Foto(imagem = nome_seguro, id_usuario = current_user.id)
            database.session.add(foto)
            database.session.commit()
        return render_template("perfil.html", usuario = current_user, form = form_foto)
    else:
        # Visualizar o perfil de outro usuário
        usuario = Usuario.query.get(int(id_usuario))
        return render_template("perfil.html", usuario = usuario, form = None)

# Sair da Página
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

# Página do Feed
@app.route("/feed")
@login_required
def feed():
    fotos = Foto.query.order_by(Foto.data_criacao.desc()).all()
    return render_template("feed.html", fotos = fotos)