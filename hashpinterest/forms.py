# Criar os Formulários do Site
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from hashpinterest.models import Usuario

class FormLogin(FlaskForm):
        email = StringField("E-mail", validators = [DataRequired(), Email()])
        senha = PasswordField("Senha", validators = [DataRequired()])
        botao_confirmacao =  SubmitField("Fazer Login")


class FormCriarConta(FlaskForm):
    email = StringField("E-mail", validators = [DataRequired(), Email()])
    username = StringField("Nome de usuário", validators = [DataRequired()])
    senha = PasswordField("Senha", validators = [DataRequired(), Length(6, 20)])
    confirmacao_senha = PasswordField("Confirmação de Senha", validators = [DataRequired(), EqualTo("senha")])
    botao_confirmacao = SubmitField("Criar Conta")

    def validate_email(self, email):
        usario = Usuario.query.filter_by(email = email.data).first()
        if usario:
            return ValidationError("E-mail já cadastrado, faça login para continuar")


class FormFoto(FlaskForm):
    foto = FileField("Foto", validators = [DataRequired()])
    botao_confirmacao = SubmitField("Enviar")