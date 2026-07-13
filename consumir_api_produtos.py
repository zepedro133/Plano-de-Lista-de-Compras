import json
from pathlib import Path
import socket
import requests

# Consumir a API de produtos
class GestorPrecos:

    def __init__(self):
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)

        url = f"http://{IPAddr}:8000/produtos"
        response = requests.get(url)

        if response.status_code == 200:
            produtos = response.json()
            #print(produtos)

            # converter lista de dicionários para dicionário de preços
            produtos = {p["nome"] + " (" + p["unidade"] + ")": p["preco"] for p in produtos}

            self.dados = produtos
           
        else:
            print("Erro ao aceder à API")
     

    def obter_preco(self, nome_produto: str) -> float | None:
        valor = self.dados.get(nome_produto)
        return float(valor) if valor is not None else None

    def listar_produtos(self) -> list[str]:
        return sorted(self.dados.keys())



# ficheiro local com os preços dos produtos
"""
class GestorPrecos:
    def __init__(self, caminho: str = "dados_produtos.json"):
        base_dir = Path(__file__).resolve().parent
        ficheiro = base_dir / caminho

        if not ficheiro.exists():
            raise FileNotFoundError(f"Não foi encontrado o ficheiro de preços: {ficheiro}")

        with ficheiro.open("r", encoding="utf-8") as f:
            self._dados = json.load(f)

    def obter_preco(self, nome_produto: str) -> float | None:
        valor = self._dados.get(nome_produto)
        return float(valor) if valor is not None else None

    def listar_produtos(self) -> list[str]:
        return sorted(self._dados.keys())
"""