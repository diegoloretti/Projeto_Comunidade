from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    SelectField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from comunidadefamilia.models import Usuario
from flask_login import current_user


class FormCriarConta(FlaskForm):
    username = StringField(
        "Nome de usuário",
        validators=[DataRequired(message="Campo obrigatório")],
        render_kw={"placeholder": "Digite o nome do seu usuário"},
    )
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Campo obrigatório"),
            Email(message="E-mail inválido"),
        ],
        render_kw={"placeholder": "Digite seu E-mail"},
    )
    sexo = SelectField(
        "Gênero",
        choices=[("Masculino", "Masculino"), ("Feminino", "Feminino")],
        validators=[DataRequired(message="Campo obrigatório")],
    )
    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="Campo obrigatório"),
            Length(6, 20, message="Senha deve ter entre 6 e 20 caracteres"),
        ],
        render_kw={"placeholder": "Digite sua Senha"},
    )
    confirmar_senha = PasswordField(
        "Confirmar da Senha",
        validators=[DataRequired(message="Campo obrigatório"), EqualTo("senha")],
        render_kw={"placeholder": "Confirme sua Senha"},
    )
    botao_submit_criarconta = SubmitField("Criar Conta")

    def validate_email(self, email):
        usuario = Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError("E-mail já cadastrado. Use outro e-mail.")


class FormLogin(FlaskForm):
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Campo obrigatório"),
            Email(message="E-mail inválido"),
        ],
        render_kw={"placeholder": "Digite seu E-mail"},
    )
    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="Campo obrigatório"),
            Length(6, 20, message="Senha deve ter entre 6 e 20 caracteres"),
        ],
        render_kw={"placeholder": "Digite sua Senha"},
    )
    lembrar_dados = BooleanField("Lembrar dados de acesso")
    botao_submit_login = SubmitField("Fazer Login")


class FormEditarPerfil(FlaskForm):
    username = StringField(
        "Nome de usuário",
        validators=[DataRequired(message="Campo obrigatório")],
    )
    email = StringField(
        "E-mail",
        validators=[
            DataRequired(message="Campo obrigatório"),
            Email(message="E-mail inválido"),
        ],
    )
    foto_perfil = FileField(
        "Foto de Perfil",
        validators=[FileAllowed(["jpg", "png"])],
    )
    sexo = SelectField(
        "Gênero",
        choices=[("Masculino", "Masculino"), ("Feminino", "Feminino")],
        validators=[DataRequired(message="Campo obrigatório")],
    )
    atrib_viagem = BooleanField("Viciado em viagem")
    atrib_estudos = BooleanField("Apaixonado por estudos")
    atrib_comida = BooleanField("Amante da boa comida")
    atrib_academia = BooleanField("Frequentador de academia")
    atrib_futebol = BooleanField("Fã de futebol")
    atrib_filmes = BooleanField("Cinéfilo")
    atrib_religiao = BooleanField("Religioso")

    botao_submit_editarperfil = SubmitField("Salvar Alterações")

    def __init__(self, *args, **kwargs):
        super(FormEditarPerfil, self).__init__(*args, **kwargs)
        if current_user.sexo == "Masculino":
            self.atrib_viagem.label.text = "Viciado em viagem"
            self.atrib_estudos.label.text = "Apaixonado por estudos"
            self.atrib_comida.label.text = "Amante da boa comida"
            self.atrib_academia.label.text = "Frequentador de academia"
            self.atrib_futebol.label.text = "Fã de futebol"
            self.atrib_filmes.label.text = "Cinéfilo"
            self.atrib_religiao.label.text = "Religioso"
        elif current_user.sexo == "Feminino":
            self.atrib_viagem.label.text = "Viciada em viagem"
            self.atrib_estudos.label.text = "Apaixonada por estudos"
            self.atrib_comida.label.text = "Amante da boa comida"
            self.atrib_academia.label.text = "Frequentadora de academia"
            self.atrib_futebol.label.text = "Fã de futebol"
            self.atrib_filmes.label.text = "Cinéfila"
            self.atrib_religiao.label.text = "Religiosa"

    def validate_email(self, email):
        if email.data != current_user.email:
            usuario = Usuario.query.filter_by(email=email.data).first()
            if usuario:
                raise ValidationError("E-mail já cadastrado. Use outro e-mail.")


class FormCriarPost(FlaskForm):
    titulo = StringField(
        "Título de post",
        validators=[DataRequired(message="Campo obrigatório"), Length(2, 140)],
    )
    conteudo = TextAreaField(
        "Escreva seu Post aqui",
        validators=[DataRequired(message="Campo obrigatório"), Length(1, 5000)],
    )
    botao_submit_criarpost = SubmitField("Criar Post")
