# Gestor de Lista de Compras (com API Local)

**Projeto desenvolvido para a unidade curricular de Linguagens de Programação - 2º Ano de Engenharia Informática.**

## 1. Resumo
Uma aplicação *desktop* desenvolvida em Python para criar e gerir listas de compras. O projeto simula um ambiente real ao consumir preços dinamicamente através de uma micro-API local (FastAPI) e garantindo a persistência do histórico de compras numa base de dados SQLite.

## 2. Como executar localmente

### Pré-requisitos
Certifica-te de que tens o Python 3.10+ instalado.
Instala as dependências necessárias executando:
```bash
pip install requests fastapi uvicorn
```

### Arranque (2 Passos)
Para o sistema funcionar, precisas de correr a API e a Aplicação em simultâneo (abre dois terminais diferentes).

**Terminal 1 (Iniciar a API de Preços):**
```bash
cd api
python main.py
```

**Terminal 2 (Iniciar a Aplicação Principal):**
```bash
python main.py
```

## 3. Funcionalidades e Objetivos
* **Cálculo Automático:** Adição e remoção de itens com atualização em tempo real dos subtotais.
* **Consumo de API:** Os preços dos produtos são obtidos dinamicamente de um catálogo JSON servido por uma API local.
* **Persistência de Dados:** Histórico de listas e itens guardados em SQLite, permitindo consultar compras passadas.
* **Interface Gráfica:** UI responsiva construída com `tkinter` e `ttk`.

## 4. Estrutura do Projeto

```text
📦 PlanoListaCompras
 ┣ 📂 api/                   # Micro-API local
 ┃ ┣ 📜 main.py              # Servidor FastAPI
 ┃ ┗ 📜 produtos.json        # Catálogo de produtos e preços
 ┣ 📂 bd/                    # Base de dados SQLite (listas.db)
 ┣ 📂 pdf/                   # Exportações e documentos
 ┣ 📜 main.py                # Aplicação Tkinter (UI + Lógica)
 ┣ 📜 modelo.py              # Classes de Domínio (Produto, ItemLista, ListaCompras)
 ┣ 📜 db.py                  # Camada de persistência (CRUD SQLite)
 ┣ 📜 consumir_api_produtos.py # Cliente HTTP para comunicação com a API
 ┗ 📜 requirements.txt       # Dependências do projeto
```

## 5. Descrição dos Componentes Principais
* **`main.py`:** Faz a orquestração da interface. Mantém a lista em memória, atualiza a *Treeview* e comunica com a base de dados para guardar o estado final.
* **`modelo.py`:** Define a estrutura de dados orientada a objetos do projeto, isolando a lógica de negócio.
* **`db.py`:** Gere o ficheiro `bd/listas.db`. Contém as tabelas `listas` e `itens` e os métodos de persistência.
* **`consumir_api_produtos.py`:** O `GestorPrecos` faz pedidos HTTP (`GET`) à API na porta 8000 e converte a resposta para consumo na UI.

## 6. Roadmap e Futuras Melhorias
Apesar de totalmente funcional, este projeto foi desenhado com espaço para evolução:
- [ ] **Segurança e Tratamento de Erros:** Adicionar tratamento robusto de exceções caso a API fique *offline* e implementar *retries*.
- [ ] **Testes:** Criação de uma *suite* de testes unitários para a lógica de negócio (`modelo.py`) e para a base de dados utilizando `sqlite3.connect(':memory:')`.
- [ ] **Portabilidade:** Melhorar a gestão de caminhos dinâmicos com `os.path.join` para garantir compatibilidade total entre Windows, macOS e Linux.
- [ ] **UX/UI:** Atualização dinâmica da combobox de produtos sem necessitar de reiniciar a aplicação.
