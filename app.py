from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    descricao = db.Column(db.String(200))

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/adicionar", methods=['GET', 'POST'])
def adicionar():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']

        novo_item = Item(nome, descricao)
        db.session.add(novo_item)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('adicionar.html')

@app.route("/listar")
def listar():
    items = Item.query.all()
    return render_template('listar.html', items=items)

@app.route("/editar/<int:item_id>", methods=['GET', 'POST'])
def editar(item_id):
    item = Item.query.get(item_id)

    if request.method == 'POST':
        item.nome = request.form['nome']
        item.descricao = request.form['descricao']

        db.session.commit()
        return redirect(url_for('listar'))

    return render_template('editar.html', item=item)

@app.route("/excluir/<int:item_id>")
def excluir(item_id):
    item = Item.query.get(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('listar'))

if __name__ == '__main__':
    app.run(debug=True)