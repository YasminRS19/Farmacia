import os

from flask import render_template, request, redirect, url_for

from ext.database import db
from model import Produto, Indicacao, Provedor

IMAGE_PATH = None


def init_app(app):
    global IMAGE_PATH
    IMAGE_PATH = app.config['UPLOAD_FOLDER']

    app.add_url_rule("/", view_func=index)
    app.add_url_rule("/produtos", view_func=index_produtos)
    app.add_url_rule("/produtos/save", view_func=produto_guardar, methods=["GET", "POST"])
    app.add_url_rule("/produtos/edit/<int:id>", view_func=produto_update, methods=["GET", "POST"])
    app.add_url_rule("/produtos/remove/<int:id>", view_func=produto_remove)

    app.add_url_rule("/provedor/save/", view_func=provedor_guardar, methods=["GET", "POST"])
    app.add_url_rule("/provedores/edit/<int:id>", view_func=provedor_editar, methods=["GET", "POST"])
    app.add_url_rule("/provedor/delete/<int:id>", view_func=provedor_eliminar, methods=["GET"])

    app.add_url_rule("/indicacoes", view_func=index_indicacoes)
    app.add_url_rule("/indicacoes/Save", view_func=indicacao_guardar, methods=["GET", "POST"])
    app.add_url_rule("/indicacoes/edit/<int:id>", view_func=indicacao_editar, methods=["GET", "POST"])
    app.add_url_rule("/indicacoes/delete/<int:id>", view_func=indicacao_eliminar, methods=["GET"])

    app.add_url_rule("/provedores", view_func=index_provedores)


def index():
    return redirect(url_for("index_produtos"))


def index_produtos():
    produtos = Produto.query.all()
    return render_template('Produtos/index_produtos.html', produtos=produtos)


# Verificar
def produto_guardar():
    provedores = Provedor.query.all()
    indicacoes = Indicacao.query.all()

    if request.method == "GET":
        return render_template('Produtos/agregar_produto.html',
                               provedores=provedores,
                               indicacoes=indicacoes)

    if request.method == "POST":
        nome = request.form['nome']
        desc = request.form['descricao']
        p_compra = request.form['preco_compra']
        p_venda = request.form['preco_venda']
        provedor_id = request.form['provedor']
        substancias = request.form['substancia']
        indicacoes2 = request.form.getlist('indicacao')

        lis_ind = [Indicacao.query.filter_by(id_indicacao=int(ind)).first() for ind in indicacoes2]

        imagem = request.files['imagem']
        fname = 'no_image.png'

        if imagem:
            fname = nome + '.png'
            basedir = os.path.abspath(os.path.dirname(__file__))
            imagem.save(os.path.join(basedir, IMAGE_PATH, fname))

        produto = Produto(
            nome=nome,
            descricao=desc,
            preco_compra=p_compra,
            preco_venda=p_venda,
            imagem=fname,
            provedor_id=provedor_id,
            substancias=substancias,
            indicacoes=lis_ind
        )

        db.session.add(produto)
        db.session.commit()

        return redirect(url_for('index_produtos'))


def produto_update(id):
    if request.method == "GET":
        prod = Produto.query.filter_by(id_produto=id).first()
        substancias = prod.substancias
        provedores = Provedor.query.all()
        indicacoes = Indicacao.query.all()

        return render_template('Produtos/editar_produto.html',
                               produto=prod, substancias=substancias, provedores=provedores,
                               indicacoes=indicacoes)

    if request.method == "POST":
        prod = Produto.query.filter_by(id_produto=id).first()

        nome = request.form['nome']
        desc = request.form['descricao']
        p_compra = request.form['preco_compra']
        p_venda = request.form['preco_venda']
        provedor_id = request.form['provedor']
        substancias = request.form['substancia']
        indicacoes = request.form.getlist('indicacao')

        lis_ind = [Indicacao.query.filter_by(id_indicacao=int(ind)).first() for ind in indicacoes]

        prod.nome = nome
        prod.descricao = desc
        prod.preco_compra = p_compra
        prod.preco_venda = p_venda
        prod.provedor_id = provedor_id
        prod.substancias = substancias
        prod.indicacoes = lis_ind

        db.session.commit()

        return redirect(url_for('index_produtos'))


def produto_remove(id):
    if id:
        try:
            prod = Produto.query.filter_by(id_produto=id).first()

            basedir = os.path.abspath(os.path.dirname(__file__))
            product_image = os.path.join(basedir, IMAGE_PATH, prod.imagem)
            os.remove(product_image)

            db.session.delete(prod)
            db.session.commit()
        except Exception as e:
            print("Erro ao apagar imagem {}".format(e))
        return redirect(url_for('index_produtos'))


def provedor_guardar():
    if request.method == "POST":
        nome = request.form['nome']
        rfc = request.form['rfc']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        provedor = Provedor(nome=nome, rfc=rfc, endereco=endereco, telefone=telefone)

        db.session.add(provedor)
        db.session.commit()

        return redirect(url_for('index_provedores'))
    if request.method == "GET":
        return render_template('Provedores/agregar_provedor.html')


def provedor_editar(id):
    provedor = Provedor.query.filter_by(id_provedor=id).first()

    if request.method == "GET":
        return render_template('Provedores/editar_provedor.html', p=provedor)

    if request.method == "POST":
        nome = request.form['nome']
        rfc = request.form['rfc']
        endereco = request.form['endereco']
        telefone = request.form['telefone']

        provedor.nome = nome
        provedor.rfc = rfc
        provedor.endereco = endereco
        provedor.telefone = telefone

        db.session.commit()

        return redirect(url_for('index_provedores'))


def provedor_eliminar(id):
    if id:
        provedor = Provedor.query.filter_by(id_provedor=id).first()

        db.session.delete(provedor)
        db.session.commit()

        return redirect(url_for('index_provedores'))


def index_indicacoes():
    indicacoes = Indicacao.query.all()

    return render_template('Indicacoes/index_indicacoes.html',
                           indicacoes=indicacoes)


def indicacao_guardar():
    if request.method == "GET":
        return render_template('Indicacoes/agregar_indicacao.html')

    if request.method == "POST":
        nome = request.form['nome']
        desc = request.form['descricao']

        indicacao = Indicacao(nome=nome, descricao=desc)

        db.session.add(indicacao)
        db.session.commit()

        return redirect(url_for('index_indicacoes'))


def indicacao_editar(id):
    indicacao = Indicacao.query.filter_by(id_indicacao=id).first()

    if request.method == "GET":
        return render_template('Indicacoes/editar_indicacao.html', i=indicacao)

    if request.method == "POST":
        nome = request.form['nome']
        desc = request.form['descricao']

        indicacao.nome = nome
        indicacao.descricao = desc

        db.session.commit()

        return redirect(url_for('index_indicacoes'))


def indicacao_eliminar(id):
    if id:
        indicacao = Indicacao.query.filter_by(id_indicacao=id).first()

        db.session.delete(indicacao)
        db.session.commit()

        return redirect(url_for('index_indicacoes'))


def index_provedores():
    provedores = Provedor.query.all()

    return render_template('Provedores/index_provedores.html',
                           provedores=provedores)
