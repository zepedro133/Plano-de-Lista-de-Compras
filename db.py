import sqlite3
import os

class BaseDados:
    def __init__(self, nome_bd: str = "listas.db"):

        #base_dir = Path(__file__).resolve().parent
        path_file = os.path.dirname(__file__) #pasta do ficheiro python
        caminho_db = os.path.join(path_file, "bd\\", nome_bd)

        self.conn = sqlite3.connect(str(caminho_db))
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.criar_tabelas()

    def criar_tabelas(self) -> None:
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS listas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            total REAL NOT NULL
        );
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lista_id INTEGER NOT NULL,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unit REAL NOT NULL,
            FOREIGN KEY(lista_id) REFERENCES listas(id) ON DELETE CASCADE
        );
        """)

        self.conn.commit()

    def guardar_lista(self, lista_compras) -> int:
        cur = self.conn.cursor()

        with self.conn:
            cur.execute(
                "INSERT INTO listas (data, total) VALUES (datetime('now','localtime'), ?);",
                (float(lista_compras.total()),)
            )
            lista_id = int(cur.lastrowid)

            for item in lista_compras.itens:
                cur.execute("""
                INSERT INTO itens (lista_id, produto, quantidade, preco_unit)
                VALUES (?, ?, ?, ?);
                """, (
                    lista_id,
                    item.produto.nome,
                    int(item.quantidade),
                    float(item.produto.preco)
                ))

        return lista_id

    def obter_ultimas_listas(self, limite: int = 10) -> list[tuple]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT id, data, total
            FROM listas
            ORDER BY id DESC
            LIMIT ?;
        """, (limite,))
        return cur.fetchall()

    def obter_itens_de_lista(self, lista_id: int) -> list[tuple]:
        cur = self.conn.cursor()
        cur.execute("""
            SELECT produto, quantidade, preco_unit
            FROM itens
            WHERE lista_id = ?
            ORDER BY id ASC;
        """, (lista_id,))
        return cur.fetchall()

    def fechar(self) -> None:
        self.conn.close()
