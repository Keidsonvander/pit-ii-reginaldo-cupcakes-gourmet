import os
import sqlite3
from contextlib import closing
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DB = os.environ.get('DATABASE_PATH', os.path.join(os.path.dirname(__file__), 'cupcakes.sqlite3'))
PRODUTOS = [
    ('Chocolate Belga', 'Cupcake de chocolate com cobertura cremosa', 14.90, '🍫'),
    ('Morango', 'Massa de baunilha e cobertura de morango', 13.90, '🍓'),
    ('Red Velvet', 'Massa vermelha e cobertura de cream cheese', 16.90, '🧁'),
    ('Baunilha', 'Massa fofinha com cobertura clássica', 12.90, '🌼'),
    ('Doce de Leite', 'Recheio e cobertura de doce de leite', 15.90, '🍮'),
    ('Limão', 'Massa cítrica e cobertura leve', 13.90, '🍋')
]

def conectar():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn

def inicializar():
    with closing(conectar()) as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY, nome TEXT NOT NULL, descricao TEXT NOT NULL, preco REAL NOT NULL CHECK(preco>0), emoji TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS pedidos (id INTEGER PRIMARY KEY AUTOINCREMENT, cliente TEXT NOT NULL, telefone TEXT NOT NULL, endereco TEXT NOT NULL, pagamento TEXT NOT NULL, total REAL NOT NULL, status TEXT NOT NULL DEFAULT 'Recebido', criado_em TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS itens_pedido (id INTEGER PRIMARY KEY AUTOINCREMENT, pedido_id INTEGER NOT NULL REFERENCES pedidos(id), produto_id INTEGER NOT NULL REFERENCES produtos(id), quantidade INTEGER NOT NULL CHECK(quantidade>0), preco_unitario REAL NOT NULL);
        """)
        if not db.execute('SELECT 1 FROM produtos LIMIT 1').fetchone():
            db.executemany('INSERT INTO produtos (nome, descricao, preco, emoji) VALUES (?,?,?,?)', PRODUTOS)
        db.commit()

@app.get('/')
def home():
    return render_template('index.html')

@app.get('/api/produtos')
def produtos():
    with closing(conectar()) as db:
        return jsonify([dict(x) for x in db.execute('SELECT * FROM produtos ORDER BY id')])

@app.post('/api/pedidos')
def pedidos():
    dados = request.get_json(silent=True) or {}
    for campo in ('cliente', 'telefone', 'endereco'):
        if not isinstance(dados.get(campo), str) or len(dados[campo].strip()) < 3:
            return jsonify(erro=f'Preencha corretamente: {campo}'), 400
    if dados.get('pagamento') not in ('Pix (simulado)', 'Cartão (simulado)', 'Boleto (simulado)'):
        return jsonify(erro='Selecione uma modalidade de pagamento'), 400
    itens = dados.get('itens')
    if not isinstance(itens, list) or not itens or len(itens) > 40:
        return jsonify(erro='Carrinho inválido'), 400
    with closing(conectar()) as db:
        conferidos = []
        for item in itens:
            if not isinstance(item, dict) or type(item.get('id')) is not int or type(item.get('quantidade')) is not int or not 1 <= item['quantidade'] <= 50:
                return jsonify(erro='Produto ou quantidade inválidos'), 400
            produto = db.execute('SELECT * FROM produtos WHERE id=?', (item['id'],)).fetchone()
            if produto is None:
                return jsonify(erro='Produto indisponível'), 400
            conferidos.append((produto, item['quantidade']))
        total_centavos = sum(round(float(p['preco'])*100)*q for p,q in conferidos)
        cur = db.execute('INSERT INTO pedidos (cliente, telefone, endereco, pagamento, total, criado_em) VALUES (?,?,?,?,?,?)', (dados['cliente'].strip()[:120], dados['telefone'].strip()[:40], dados['endereco'].strip()[:250], dados['pagamento'],total_centavos/100,datetime.now(timezone.utc).isoformat()))
        db.executemany('INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?,?,?,?)', [(cur.lastrowid,p['id'],q,p['preco']) for p,q in conferidos])
        db.commit()
        return jsonify(numero=cur.lastrowid,total=total_centavos/100,status='Recebido',aviso='Pagamento demonstrativo: nenhuma cobrança foi realizada.'), 201

@app.get('/api/pedidos/<int:numero>')
def consultar_pedido(numero):
    telefone = request.args.get('telefone','').strip()
    if not telefone:
        return jsonify(erro='Informe o telefone usado no pedido'), 400
    with closing(conectar()) as db:
        pedido = db.execute('SELECT id, status, total, pagamento, criado_em FROM pedidos WHERE id=? AND telefone=?', (numero,telefone)).fetchone()
        if not pedido:
            return jsonify(erro='Pedido não encontrado'), 404
        return jsonify(dict(pedido))

inicializar()

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG') == '1')
