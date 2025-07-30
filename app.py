from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'instance')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(UPLOAD_FOLDER, 'marcas.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Marca(db.Model):
    numero_processo = db.Column(db.String(50), primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    titular = db.Column(db.String(100))
    classe = db.Column(db.String(50))
    especificacoes = db.Column(db.Text)
    status = db.Column(db.String(50))
    observacoes = db.Column(db.Text)
    vendedor = db.Column(db.String(100))
    comprador = db.Column(db.String(100))
    arquivo = db.Column(db.String(200))

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/marcas', methods=['GET'])
def listar_resumo():
    marcas = Marca.query.all()
    return jsonify([{
        'numero_processo': m.numero_processo,
        'nome': m.nome,
        'titular': m.titular,
        'classe': m.classe,
        'status': m.status,
        'especificacoes': m.especificacoes,
        'observacoes': m.observacoes,
        'vendedor': m.vendedor,
        'comprador': m.comprador,
        'arquivo': m.arquivo
    } for m in marcas])

@app.route('/marca/<string:numero_processo>', methods=['GET'])
def detalhar_marca(numero_processo):
    marca = Marca.query.get_or_404(numero_processo)
    return jsonify({
        'numero_processo': marca.numero_processo,
        'nome': marca.nome,
        'titular': marca.titular,
        'classe': marca.classe,
        'especificacoes': marca.especificacoes,
        'status': marca.status,
        'observacoes': marca.observacoes,
        'vendedor': marca.vendedor,
        'comprador': marca.comprador,
        'arquivo': marca.arquivo
    })

@app.route('/marca', methods=['POST'])
def adicionar_marca():
    dados = request.form
    arquivo = request.files.get('arquivo')

    if Marca.query.get(dados['numero_processo']):
        return jsonify({'error': 'Número do processo já existe.'}), 400

    filename = None
    if arquivo and arquivo.filename:
        filename = arquivo.filename
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    marca = Marca(
        numero_processo=dados['numero_processo'],
        nome=dados['nome'],
        titular=dados.get('titular'),
        classe=dados.get('classe'),
        especificacoes=dados.get('especificacoes'),
        status=dados.get('status'),
        observacoes=dados.get('observacoes'),
        vendedor=dados.get('vendedor'),
        comprador=dados.get('comprador'),
        arquivo=filename
    )
    db.session.add(marca)
    db.session.commit()
    return jsonify({'message': 'Marca adicionada com sucesso!'}), 201

@app.route('/marca/<string:numero_processo>', methods=['PUT'])
def atualizar_marca(numero_processo):
    marca = Marca.query.get_or_404(numero_processo)
    dados = request.form
    arquivo = request.files.get('arquivo')

    if arquivo and arquivo.filename:
        filename = arquivo.filename
        arquivo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        marca.arquivo = filename

    marca.nome = dados.get('nome', marca.nome)
    marca.titular = dados.get('titular', marca.titular)
    marca.classe = dados.get('classe', marca.classe)
    marca.especificacoes = dados.get('especificacoes', marca.especificacoes)
    marca.status = dados.get('status', marca.status)
    marca.observacoes = dados.get('observacoes', marca.observacoes)
    marca.vendedor = dados.get('vendedor', marca.vendedor)
    marca.comprador = dados.get('comprador', marca.comprador)

    db.session.commit()
    return jsonify({'message': 'Marca atualizada com sucesso!'})

@app.route('/marca/<string:numero_processo>', methods=['DELETE'])
def deletar_marca(numero_processo):
    marca = Marca.query.get_or_404(numero_processo)
    db.session.delete(marca)
    db.session.commit()
    return jsonify({'message': 'Marca excluída com sucesso!'})

@app.route('/uploads/<filename>')
def baixar_arquivo(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
