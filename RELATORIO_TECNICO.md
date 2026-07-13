# Relatório Técnico — Planeamento de Lista de Compras

## 1. Resumo
Projeto em Python para criar, gerir e armazenar listas de compras com preços obtidos através de uma API local. Interface gráfica em Tkinter para adicionar/remover itens, visualizar subtotais e guardar listas numa base de dados SQLite.

## 2. Objetivos
- Permitir ao utilizador criar listas de compras com cálculo automático de preços.
- Obter preços de uma API local (`api/produtos.json` via `api/main.py`).
- Persistir listas e itens em SQLite (`bd/listas.db`).
- Interface simples e responsiva com validações básicas.

## 3. Estrutura do projecto
- [main.py](main.py): Aplicação Tkinter (UI + lógica de interação).
- [modelo.py](modelo.py): Classes de domínio (`Produto`, `ItemLista`, `ListaCompras`).
- [db.py](db.py): Camada de persistência com SQLite (criação de tabelas, guardar/ler listas).
- [consumir_api_produtos.py](consumir_api_produtos.py): Cliente que consome a API de preços.
- [notas.txt](notas.txt): Instruções rápidas para executar.
- `api/`: micro-API local em FastAPI
  - [api/main.py](api/main.py): servidor FastAPI que serve `produtos.json`.
  - [api/produtos.json](api/produtos.json): ficheiro JSON com catálogo de produtos e preços.
- `bd/`: pasta onde é criado o ficheiro SQLite (via `db.py`).

## 4. Descrição dos componentes
- main.py
  - UI construída com `tkinter` e `ttk`.
  - Interação com `GestorPrecos` para listar produtos e obter preços.
  - Mantém `ListaCompras` em memória e atualiza `Treeview` e total.
  - Operações: adicionar, remover, limpar, guardar (persistir no BD), ver histórico.

- modelo.py
  - `Produto`: nome e preço.
  - `ItemLista`: associação produto + quantidade e cálculo do subtotal.
  - `ListaCompras`: colecção de itens e soma do total.

- db.py
  - Usa `sqlite3` e guarda o ficheiro em `bd/listas.db` (caminho relativo a `db.py`).
  - Tabelas: `listas(id, data, total)` e `itens(id, lista_id, produto, quantidade, preco_unit)`.
  - Funções principais: `guardar_lista`, `obter_ultimas_listas`, `obter_itens_de_lista`.

- consumir_api_produtos.py
  - `GestorPrecos` obtém a lista de produtos ao consultar `http://<IP>:8000/produtos`.
  - Converte a resposta JSON num dicionário {"nome (unidade)": preco}.
  - Métodos: `listar_produtos()` e `obter_preco(nome)`.
  - Existe código comentado para carregar preços de ficheiro local como alternativa.

- api/main.py e api/produtos.json
  - Servidor FastAPI que expõe rotas `/` e `/produtos` e `/produtos/{id}`.
  - `produtos.json` contém um catálogo de 60 itens (id, nome, preco, unidade).

## 5. Fluxo de execução
1. Iniciar a API local: abrir `api` e executar `python main.py` (ou `uvicorn api.main:app --host 0.0.0.0 --port 8000`).
2. Iniciar a aplicação principal: executar `python main.py` na raiz do projeto.
3. A aplicação carrega produtos via `GestorPrecos` e popula a combobox.
4. Utilizador adiciona itens; ao guardar, `db.BaseDados.guardar_lista` persiste a lista e itens.

## 6. Requisitos e dependências
- Python 3.10+ recomendado (uso de typing `list[ItemLista]` e `|` para union).
- Dependências externas:
  - `requests` (consumo da API)
  - `fastapi`, `uvicorn` (apenas para a API, pasta `api/`)
- Biblioteca padrão: `tkinter`, `sqlite3`, `json`, `os`, `socket`.

## 7. Observações técnicas e pontos de melhoria
- Robustez da API:
  - `consumir_api_produtos.py` assume que a API está disponível no IP da máquina; em redes com NAT/IPv6 ou firewalls pode falhar.
  - Adicionar tratamento de exceções mais detalhado e reconexão/regeneração de cache.

- Validação e UX:
  - A combobox é preenchida apenas no arranque; tornar atualizável dinamicamente.
  - Melhorar mensagens de erro e internacionalização (i18n) caso seja necessário.

- Persistência:
  - Atualmente o caminho do BD usa `bd\listas.db` concatenado a `__file__` — é funcional no Windows, mas usar `os.path.join(path_file, 'bd', nome_bd)` torna-o multiplataforma.
  - Adicionar migrações ou versão do esquema para futuras alterações.

- Testes e CI:
  - Falta suíte de testes automáticos. Recomenda-se criar testes para `modelo.py` e para `db.py` (usando BD em memória `sqlite3.connect(':memory:')`).

- Segurança:
  - A API não tem autenticação; aceitável para demonstração local, mas não para produção.

- Código e estilo:
  - Alguns comentários e código comentado podem ser limpos.
  - Tipagem pode ser reforçada com `typing`/`pydantic` para a API.

## 8. Como executar localmente (passos rápidos)
No terminal 1 (API):
```bash
cd api
python main.py
```
No terminal 2 (App):
```bash
cd ..
python main.py
```
Observações: instalar dependências se necessário:
```bash
pip install requests fastapi uvicorn
```

## 9. Conclusão
Projeto bem estruturado para um mini-projeto: separação clara entre domínio (`modelo.py`), persistência (`db.py`), consumo de API (`consumir_api_produtos.py`) e interface (`main.py`). Para evolução rumo a produção, adicionar testes, tratamento de erros, configuração de ambiente e melhorias de portabilidade e segurança.
