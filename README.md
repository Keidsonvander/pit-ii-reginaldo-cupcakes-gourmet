# PIT II — Cupcakes Gourmet

**Aluno:** Reginaldo Oliveira da Silva  
**RGM:** 33091544  
**Disciplina:** Projeto Integrador Transdisciplinar em Engenharia de Software II

Aplicativo web responsivo desenvolvido como continuidade do planejamento da PIT I.

## Funcionalidades implementadas
- Catálogo de seis sabores com busca.
- Carrinho, alteração de quantidades e cálculo do total.
- Formulário para registro de pedidos com nome, telefone e endereço.
- Consulta de pedidos pelo número e telefone.
- Armazenamento em banco SQLite.
- Opções de pagamento simuladas, sem cobrança real.

**Limitações:** ainda não há cadastro/autenticação de clientes, pagamentos reais ou rastreamento de entrega. Os testes com cinco avaliadores e o laudo de qualidade ainda precisam ser realizados.

## Tecnologias
Python 3, Flask, SQLite, HTML, CSS e JavaScript. Codificação tradicional.

## Execução local
```bash
python -m venv .venv
pip install -r requirements.txt
python app.py
```
Acesse http://127.0.0.1:5000.

## Hospedagem
Há um `Procfile` para iniciar via Gunicorn. Build: `pip install -r requirements.txt`; start: `gunicorn app:app`. A implantação depende da configuração de um serviço de hospedagem. Para manter pedidos salvos, é necessário armazenamento persistente, pois o arquivo SQLite local pode ser perdido em hospedagem efêmera.

## Documentação
Consulte `docs/escopo.md` e `docs/testes.md`. A publicação do vídeo narrado e a avaliação por cinco pessoas são etapas pendentes.
