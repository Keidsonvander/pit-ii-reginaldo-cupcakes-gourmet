import os
import tempfile
import unittest

class CupcakesTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        os.environ['DATABASE_PATH'] = os.path.join(self.tmp.name, 'teste.sqlite3')
        import importlib
        import app
        self.mod = importlib.reload(app)
        self.client = self.mod.app.test_client()

    def tearDown(self):
        self.tmp.cleanup()

    def test_catalogo(self):
        resposta = self.client.get('/api/produtos')
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(len(resposta.json), 6)

    def test_pedido_e_consulta(self):
        pedido = {'cliente':'Cliente Teste', 'telefone':'11999999999', 'endereco':'Rua das Flores, 10', 'pagamento':'Pix (simulado)', 'itens':[{'id':1,'quantidade':2}]}
        resposta = self.client.post('/api/pedidos',json=pedido)
        self.assertEqual(resposta.status_code,201)
        numero = resposta.json['numero']
        consulta = self.client.get(f'/api/pedidos/{numero}?telefone=11999999999')
        self.assertEqual(consulta.status_code,200)

    def test_rejeitar_carrinho_vazio(self):
        resposta = self.client.post('/api/pedidos',json={'cliente':'Cliente Teste','telefone':'11999999999','endereco':'Rua das Flores','pagamento':'Pix (simulado)','itens':[]})
        self.assertEqual(resposta.status_code,400)

if __name__ == '__main__':
    unittest.main()
