import tkinter as tk
from tkinter import ttk, messagebox

from modelo import Produto, ItemLista, ListaCompras
from consumir_api_produtos import GestorPrecos
from db import BaseDados


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Planeamento de Lista de Compras")
        self.geometry("980x600")
        self.minsize(920, 560)

        self.api = GestorPrecos()
        self.bd = BaseDados()
        self.lista = ListaCompras()

        self.cores = {
            "BG_MAIN": "#1e1f22",
            "BG_CARD": "#2b2d31",
            "BG_SEC": "#313338",
            "FG_TEXT": "#dbdee1",
            "FG_MUTED": "#949ba4",
            "ACCENT": "#06ff2b",
            "SELECTED": "#5865f2",
            "BORDER": "#3f4147",
            "BTN_HOVER": "#0e0f11",
            "ACCENT_HOVER": "#047a16",
            "ACCENT_REMOVE": "#ff073a",
            "ACCENT_OTHER": "#252527",
            "REMOVE_HOVER": "#5a0315",
        }

        self.configurar_estilos()
        self.criar_ui()
        self.atualizar_total()
        self.carregar_historico()

    # ---------------- ESTILOS ----------------

    def configurar_estilos(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        c = self.cores
        self.configure(bg=c["BG_MAIN"])

        style.configure("TFrame", background=c["BG_MAIN"])
        style.configure("Card.TFrame", background=c["BG_CARD"], padding=12)

        style.configure("TLabel", background=c["BG_MAIN"], foreground=c["FG_TEXT"])
        style.configure(
            "Header.TLabel",
            background=c["BG_CARD"],
            foreground=c["FG_TEXT"],
            font=("Segoe UI", 11, "bold"),
        )
        style.configure(
            "Total.TLabel",
            background=c["BG_MAIN"],
            foreground=c["FG_TEXT"],
            font=("Segoe UI", 14, "bold"),
        )

        style.configure(
            "TButton",
            background=c["BG_CARD"],
            foreground=c["FG_TEXT"],
            padding=6,
            relief="flat",
        )
        style.map("TButton", background=[("active", c["BTN_HOVER"])])

        style.configure(
            "Primary.TButton",
            background=c["ACCENT"],
            foreground="white",
            font=("Segoe UI", 10, "bold"),
        )
        style.map("Primary.TButton", background=[("active", c["ACCENT_HOVER"])])

        style.configure(
            "Secondary.TButton",
            background=c["ACCENT_OTHER"],
            foreground=c["FG_TEXT"],
            font=("Segoe UI", 10),
            relief="flat",
        )
        style.map("Secondary.TButton", background=[("active", c["BTN_HOVER"])])

        style.configure(
            "Remove.TButton",
            background=c["ACCENT_REMOVE"],
            foreground=c["FG_TEXT"],
            font=("Segoe UI", 10),
            relief="flat",
        )
        style.map("Remove.TButton", background=[("active", c["REMOVE_HOVER"])])

        # style.configure(
        #     "TCombobox",
        #     fieldbackground=c["BG_SEC"],
        #     background=c["BG_SEC"],
        #     foreground=c["FG_TEXT"],
        #     arrowcolor=c["FG_TEXT"],
        # )

        # style.configure(
        #     "TSpinbox",
        #     fieldbackground=c["BG_SEC"],
        #     background=c["BG_SEC"],
        #     foreground=c["FG_TEXT"],
        #     arrowcolor=c["FG_TEXT"],
        # )

        style.configure(
            "Treeview",
            background=c["BG_SEC"],
            foreground=c["FG_TEXT"],
            fieldbackground=c["BG_SEC"],
            bordercolor=c["BORDER"],
            rowheight=26,
        )
        style.configure(
            "Treeview.Heading",
            background=c["BG_CARD"],
            foreground=c["FG_TEXT"],
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            borderwidth=0,
        )
        style.map(
            "Treeview",
            background=[("selected", c["SELECTED"])],
            foreground=[("selected", "white")],
        )

    # ---------------- UI ----------------

    def criar_ui(self):
        c = self.cores

        topo = ttk.Frame(self, style="Card.TFrame")
        topo.pack(fill="x", padx=12, pady=(12, 8))

        ttk.Label(topo, text="Adicionar item", style="Header.TLabel").grid(
            row=0, column=0, columnspan=8, sticky="w", pady=(0, 8)
        )

        ttk.Label(topo, text="Produto").grid(row=1, column=0, sticky="w")
        self.cmb_produto = ttk.Combobox(
            topo,
            values=self.api.listar_produtos(),
            state="readonly",
            width=38,
        )
      
        self.cmb_produto.grid(row=2, column=0, padx=(0, 12), sticky="we")
        if self.cmb_produto["values"]:
            self.cmb_produto.set(self.cmb_produto["values"][0])

        ttk.Label(topo, text="Quantidade").grid(row=1, column=1, sticky="w")
        self.spn_quant = ttk.Spinbox(topo, from_=1, to=99, width=8)
        self.spn_quant.grid(row=2, column=1, padx=(0, 12), sticky="w")
        self.spn_quant.set(1)

        ttk.Button(topo, text="Adicionar", style="Primary.TButton", command=self.adicionar).grid(
            row=2, column=2, padx=(0, 8)
        )
        ttk.Button(topo, text="Remover", style="Remove.TButton", command=self.remover).grid(
            row=2, column=3, padx=(0, 8)
        )
        ttk.Button(topo, text="Limpar", style="Secondary.TButton", command=self.limpar).grid(
            row=2, column=4, padx=(0, 8)
        )
        ttk.Button(topo, text="Guardar (BD)", style="Secondary.TButton", command=self.guardar).grid(
            row=2, column=5
        )

        topo.columnconfigure(0, weight=1)

        corpo = ttk.Frame(self)
        corpo.pack(fill="both", expand=True, padx=12, pady=(0, 8))

        esquerda = ttk.Frame(corpo, style="Card.TFrame")
        esquerda.pack(side="left", fill="both", expand=True, padx=(0, 8))

        ttk.Label(esquerda, text="Itens da lista", style="Header.TLabel").pack(anchor="w", pady=(0, 6))

        cols = ("produto", "quantidade", "preco_unit", "subtotal")
        self.tree = ttk.Treeview(esquerda, columns=cols, show="headings", height=14)

        self.tree.heading("produto", text="Produto")
        self.tree.heading("quantidade", text="Qtd.")
        self.tree.heading("preco_unit", text="Preço unit. (€)")
        self.tree.heading("subtotal", text="Subtotal (€)")

        self.tree.column("produto", width=360, anchor="w")
        self.tree.column("quantidade", width=70, anchor="center")
        self.tree.column("preco_unit", width=140, anchor="e")
        self.tree.column("subtotal", width=140, anchor="e")

        self.tree.tag_configure("odd", background="#2b2d31")
        self.tree.tag_configure("even", background="#313338")

        self.tree.pack(side="left", fill="both", expand=True)

        direita = ttk.Frame(corpo, style="Card.TFrame")
        direita.pack(side="right", fill="y")

        ttk.Label(direita, text="Histórico", style="Header.TLabel").pack(anchor="w")
        ttk.Label(direita, text="Últimas listas guardadas (BD)").pack(anchor="w", pady=(0, 6))

        self.lst_historico = tk.Listbox(
            direita,
            height=16,
            width=40,
            bg=c["BG_SEC"],
            fg=c["FG_TEXT"],
            selectbackground=c["SELECTED"],
            selectforeground="white",
            relief="flat",
            highlightthickness=1,
            highlightbackground=c["BORDER"],
        )
        self.lst_historico.pack(pady=(0, 8))

        ttk.Button(direita, text="Ver detalhes", style="Secondary.TButton", command=self.ver_detalhes).pack(fill="x")

        fundo = ttk.Frame(self, style="Card.TFrame")
        fundo.pack(fill="x", padx=12, pady=(0, 12))

        ttk.Label(
            fundo,
            text="Dica: escolhe o produto e ajusta a quantidade. Enter adiciona.",
        ).pack(side="left")

        self.lbl_total = ttk.Label(fundo, text="Total: 0.00 €", style="Total.TLabel")
        self.lbl_total.pack(side="right")

        self.bind("<Return>", lambda _e: self.adicionar())
        self.bind("<Delete>", lambda _e: self.remover())

        self.cmb_produto.set("")

    # ---------------- LÓGICA ----------------

    def adicionar(self):
        nome = self.cmb_produto.get().strip()
        qtd_txt = str(self.spn_quant.get()).strip()

        if not nome:
            messagebox.showwarning("Validação", "Seleciona um produto.")
            return
        if not qtd_txt.isdigit() or int(qtd_txt) <= 0:
            messagebox.showwarning("Validação", "Quantidade inválida.")
            return

        quantidade = int(qtd_txt)
        preco = self.api.obter_preco(nome)
        if preco is None:
            messagebox.showerror("Erro", f"Não existe preço para '{nome}'.")
            return

        produto = Produto(nome, preco)
        item = ItemLista(produto, quantidade)
        self.lista.adicionar_item(item)

        tag = "odd" if len(self.tree.get_children()) % 2 == 0 else "even"
        self.tree.insert(
            "",
            "end",
            values=(produto.nome, quantidade, f"{preco:.2f}", f"{item.total():.2f}"),
            tags=(tag,),
        )

        self.atualizar_total()
        self.spn_quant.set(1)
        self.cmb_produto.set("")

    def remover(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Validação", "Seleciona um produto.")
            return
        
        idx = self.tree.index(sel[0])
        self.tree.delete(sel[0])
        self.lista.remover_indice(idx)
        self.atualizar_total()

    def limpar(self):
        if not self.lista.itens:
            messagebox.showwarning("Validação", "A lista está vazia.")
            return
        if not messagebox.askyesno("Limpar", "Queres limpar a lista toda?"):
            return
        self.tree.delete(*self.tree.get_children())
        self.lista.limpar()
        self.atualizar_total()

    def guardar(self):
        if not self.lista.itens:
            messagebox.showwarning("Validação", "A lista está vazia.")
            return
        self.bd.guardar_lista(self.lista)
        self.carregar_historico()
        self.tree.delete(*self.tree.get_children())
        self.lista.limpar()
        self.atualizar_total()

    def carregar_historico(self):
        self.lst_historico.delete(0, tk.END)
        self.historico_map = []
        for lista_id, data, total in self.bd.obter_ultimas_listas(10):
            self.historico_map.append((lista_id, data))
            self.lst_historico.insert(tk.END, f"#{lista_id} | {data} | {total:.2f} €")

    def ver_detalhes(self):
        sel = self.lst_historico.curselection()
        if not sel:
            messagebox.showwarning("Validação", "Seleciona uma lista no histórico.")
            return
        lista_id, _ = self.historico_map[sel[0]]
        itens = self.bd.obter_itens_de_lista(lista_id)

        texto = []
        for prod, qtd, preco in itens:
            texto.append(f"- {prod}: {qtd} x {preco:.2f} €")

        messagebox.showinfo("Detalhes da lista", "\n".join(texto))

    def atualizar_total(self):
        self.lbl_total.config(text=f"Total: {self.lista.total():.2f} €")


if __name__ == "__main__":
    App().mainloop()
