# pip install fastapi uvicorn
from fastapi import FastAPI ##a
import json
import uvicorn ##a
import socket
import os

##path = os.getcwd() #pasta corrente - S1 - Linguagens de Programação
##path_file = os.path.dirname(__file__) #pasta do ficheiro python
##print(path)
##print(path_file)

app = FastAPI(
    title="API de Preços de Produtos",
    description="API simples para disponibilizar preços de produtos em JSON",
    version="1.0.0"
)

path_file = os.path.dirname(__file__) #pasta do ficheiro python
path_file_json = os.path.join(path_file, "produtos.json")

try:
    with open(path_file_json, 'r', encoding='utf-8') as file:
        produtos = json.load(file)
except:
    print("Erro ao abrir o ficheiro.")
else:           

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)

    #print("Your Computer Name is:", hostname)
    #print("Your Computer IP Address is:", IPAddr)


    @app.get("/", tags=["Geral"])
    async def root():
        """Rota inicial de boas-vindas."""
        return [{"mensagem": "Bem-vindo à API de Produtos!"},
                {"rotas":"http://" + IPAddr + ":8000/produtos | http://" + IPAddr + ":8000/produtos/id"}]


    @app.get("/produtos")
    def listar_produtos():
        return produtos

    @app.get("/produtos/{produto_id}")
    def obter_produto(produto_id: int):
        for produto in produtos:
            if produto["id"] == produto_id:
                return produto
        return {"erro": "Produto não encontrado"}


    # Bloco para execução
    if __name__ == "__main__":
        # O servidor ficará disponível em http://127.0.0.1:8000
        # uvicorn.run(app, host="127.0.0.1", port=8000)
        uvicorn.run(app, host=IPAddr , port=8000)
