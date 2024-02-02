from comunidadefamilia import database, login_manager
from datetime import datetime
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))


class Usuario(database.Model, UserMixin):
    id = database.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    senha = database.Column(database.String, nullable=False)
    foto_perfil = database.Column(database.String, default="default.jpg")
    posts = database.relationship("Post", backref="autor", lazy=True)
    sexo = database.Column(database.String, nullable=False)
    atributos = database.Column(
        database.String, nullable=False, default="Não informado"
    )

    def contar_posts(self):
        return len(self.posts)


class Post(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    titulo = database.Column(database.String, nullable=False)
    conteudo = database.Column(database.Text, nullable=False)
    data_postagem = database.Column(
        database.DateTime, nullable=False, default=datetime.utcnow
    )
    usuario_id = database.Column(
        database.Integer, database.ForeignKey("usuario.id"), nullable=False
    )
