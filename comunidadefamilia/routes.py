from flask import render_template, url_for, flash, redirect, request, abort
from comunidadefamilia import app, database, bcrypt
from comunidadefamilia.forms import (
    FormCriarConta,
    FormLogin,
    FormEditarPerfil,
    FormCriarPost,
)
from comunidadefamilia.models import Usuario, Post
from flask_login import login_user, current_user, logout_user, login_required
from PIL import Image
import secrets
import os


@app.route("/")
def home():
    posts = Post.query.order_by(Post.data_postagem.desc()).all()
    return render_template("home.html", posts=posts)


@app.route("/usuarios")
@login_required
def usuarios():
    lista_usuarios = Usuario.query.all()
    return render_template(
        "usuarios.html",
        lista_usuarios=lista_usuarios,
    )


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form_login = FormLogin()
    form_criarconta = FormCriarConta()
    if form_login.validate_on_submit() and form_login.botao_submit_login.data:
        usuario = Usuario.query.filter_by(email=form_login.email.data).first()
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(usuario, remember=form_login.lembrar_dados.data)
            flash(
                f"Login realizado com sucesso no e-mail: {form_login.email.data}",
                category="alert-success",
            )
            proxima_pagina = request.args.get("next")
            redirects_seguros = [
                "/",
                "/contato",
                "/usuarios",
                "/perfil",
                "/login",
                "/post/criar",
            ]
            if proxima_pagina in redirects_seguros:
                return redirect(proxima_pagina)
            else:
                return redirect(url_for("home"))
        else:
            flash(
                f"Login não realizado. Verifique o e-mail e senha digitados.",
                category="alert-danger",
            )
    if (
        form_criarconta.validate_on_submit()
        and form_criarconta.botao_submit_criarconta.data
    ):
        senha_cript = bcrypt.generate_password_hash(form_criarconta.senha.data).decode(
            "utf-8"
        )
        usuario = Usuario(
            username=form_criarconta.username.data,
            email=form_criarconta.email.data,
            senha=senha_cript,
            sexo=form_criarconta.sexo.data,
        )
        database.session.add(usuario)
        database.session.commit()
        flash(
            f"Login realizado com sucesso no e-mail: {form_criarconta.email.data}",
            category="alert-success",
        )
        return redirect(url_for("home"))
    return render_template(
        "logincriar.html", form_login=form_login, form_criarconta=form_criarconta
    )


@app.route("/logout")
@login_required
def sair():
    logout_user()
    flash("Logout realizado com sucesso.", category="alert-success")
    return redirect(url_for("home"))


@app.route("/perfil")
@login_required
def perfil():
    foto_perfil = url_for("static", filename=f"fotos_perfil/{current_user.foto_perfil}")
    return render_template("perfil.html", foto_perfil=foto_perfil)


def salvar_imagem(imagem, user_id):
    nome, extensao = os.path.splitext(imagem.filename)
    nome_imagem = f"{user_id}{extensao}"
    caminho_completo = os.path.join(app.root_path, "static/fotos_perfil", nome_imagem)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail((200, 200))
    imagem_reduzida.save(caminho_completo)
    return nome_imagem


def atualizar_atributos(form):
    atributos = []
    for atributo in form:
        if "atrib_" in atributo.name:
            if atributo.data:
                atributos.append(atributo.label.text)
    atributos = ";".join(atributos)
    if len(atributos) == 0:
        atributos = "Não informado"
    return atributos


@app.route("/perfil/editar", methods=["GET", "POST"])
@login_required
def editar_perfil():
    form = FormEditarPerfil()
    foto_perfil = url_for("static", filename=f"fotos_perfil/{current_user.foto_perfil}")
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.sexo = form.sexo.data
        if form.foto_perfil.data:
            nome_imagem = salvar_imagem(form.foto_perfil.data, current_user.id)
            current_user.foto_perfil = nome_imagem
        current_user.atributos = atualizar_atributos(form)
        database.session.commit()
        flash(f"Perfil atualizado com sucesso.", category="alert-success")
        return redirect(url_for("perfil"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.sexo.data = current_user.sexo
        if current_user.atributos:
            atributos = current_user.atributos.split(";")
            for atributo in atributos:
                if "viagem" in atributo:
                    form.atrib_viagem.data = True
                if "estudos" in atributo:
                    form.atrib_estudos.data = True
                if "comida" in atributo:
                    form.atrib_comida.data = True
                if "academia" in atributo:
                    form.atrib_academia.data = True
                if "futebol" in atributo:
                    form.atrib_futebol.data = True
                if "Cinéfil" in atributo:
                    form.atrib_filmes.data = True
                if "Religioso" in atributo:
                    form.atrib_religiao.data = True
    return render_template("editar_perfil.html", foto_perfil=foto_perfil, form=form)


@app.route("/post/criar", methods=["GET", "POST"])
@login_required
def criar_post():
    form = FormCriarPost()
    if form.validate_on_submit():
        post = Post(
            titulo=form.titulo.data, conteudo=form.conteudo.data, autor=current_user
        )
        database.session.add(post)
        database.session.commit()
        flash(f"Post criado com sucesso.", category="alert-success")
        return redirect(url_for("home"))
    return render_template("criar_post.html", form=form)


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def exibir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        form = FormCriarPost()
        form.botao_submit_criarpost.label.text = "Atualizar Post"
        if request.method == "GET":
            form.titulo.data = post.titulo
            form.conteudo.data = post.conteudo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data
            post.conteudo = form.conteudo.data
            database.session.commit()
            flash(f"Post atualizado com sucesso.", category="alert-success")
            return redirect(url_for("home"))
    else:
        form = None
    return render_template("post.html", post=post, form=form)


@app.route("/post/<int:post_id>/excluir", methods=["GET", "POST"])
@login_required
def excluir_post(post_id):
    post = Post.query.get(post_id)
    if current_user == post.autor:
        database.session.delete(post)
        database.session.commit()
        flash(f"Post excluído com sucesso.", category="alert-danger")
        return redirect(url_for("home"))
    else:
        abort(403)
