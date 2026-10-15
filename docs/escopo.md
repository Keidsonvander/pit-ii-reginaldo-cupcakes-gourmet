# Escopo e requisitos — PIT II

Aluno: Reginaldo Oliveira da Silva — RGM 33091544.

## Origem
Continuação da PIT I, situação-problema 1: aplicativo de vendas de cupcakes gourmet.

## Requisitos funcionais
- RF01: exibir catálogo de cupcakes, sabores, descrições e preços.
- RF02: pesquisar produtos por nome.
- RF03: adicionar e remover itens do carrinho.
- RF04: calcular o valor dos itens selecionados.
- RF05: receber nome, telefone e endereço.
- RF06: registrar o pedido no banco de dados.
- RF07: permitir consulta de pedido por número e telefone.
- RF08: apresentar formas de pagamento como simulação.

## Requisitos não funcionais
- RNF01: interface responsiva e com linguagem acessível.
- RNF02: validação das entradas no servidor.
- RNF03: integridade referencial para itens do pedido.
- RNF04: persistência de dados em SQLite.
- RNF05: uso de parâmetros SQL, sem concatenar entrada do usuário.

## Modelo lógico
Produtos(id PK, nome, descricao, preco, emoji).
Pedidos(id PK, cliente, telefone, endereco, pagamento, total, status, criado_em).
Itens_pedido(id PK, pedido_id FK, produto_id FK, quantidade, preco_unitario).

## Pendências para versão completa da PIT I
Autenticação real do cliente, pagamento integrado e acompanhamento logístico real não estão implementados nesta demonstração.

## Observações
Os feedbacks de cinco avaliadores e as evidências do laudo deverão ser coletados após o software ser testado.
