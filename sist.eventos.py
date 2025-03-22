import tkinter as tk
from tkinter import messagebox
import sqlite3
import os

# Funções de Banco de Dados
def criar_banco_dados():
    try:
        caminho_banco_dados = os.path.join(os.getcwd(), 'eventos_academicos.db')
        with sqlite3.connect(caminho_banco_dados) as conexao:
            cursor = conexao.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS eventos
                             (id INTEGER PRIMARY KEY AUTOINCREMENT,
                              titulo TEXT NOT NULL,
                              descricao TEXT NOT NULL,
                              data TEXT NOT NULL)''')
            conexao.commit()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar banco de dados: {e}")

def adicionar_evento(titulo, descricao, data):
    try:
        caminho_banco_dados = os.path.join(os.getcwd(), 'eventos_academicos.db')
        with sqlite3.connect(caminho_banco_dados) as conexao:
            cursor = conexao.cursor()
            cursor.execute("INSERT INTO eventos (titulo, descricao, data) VALUES (?, ?, ?)", (titulo, descricao, data))
            conexao.commit()
            return True
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao adicionar evento: {e}")
        return False

def mostrar_eventos():
    try:
        caminho_banco_dados = os.path.join(os.getcwd(), 'eventos_academicos.db')
        with sqlite3.connect(caminho_banco_dados) as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM eventos")
            return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar eventos: {e}")
        return []

def buscar_eventos(palavra_chave):
    try:
        caminho_banco_dados = os.path.join(os.getcwd(), 'eventos_academicos.db')
        with sqlite3.connect(caminho_banco_dados) as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT * FROM eventos WHERE titulo LIKE ? OR descricao LIKE ?",
                           (f"%{palavra_chave}%", f"%{palavra_chave}%"))
            return cursor.fetchall()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar eventos: {e}")
        return []

# Funções da Interface Gráfica
def adicionar_evento_interface():
    titulo = entrada_titulo.get()
    descricao = entrada_descricao.get()
    data = entrada_data.get()

    if adicionar_evento(titulo, descricao, data):
        messagebox.showinfo("Sucesso", "Evento adicionado com sucesso!")
    else:
        messagebox.showerror("Erro", "Não foi possível adicionar o evento.")

def mostrar_eventos_interface():
    eventos = mostrar_eventos()
    if eventos:
        eventos_texto = "\n".join([f"{evento[1]} - {evento[2]} em {evento[3]}" for evento in eventos])
        messagebox.showinfo("Eventos", eventos_texto)
    else:
        messagebox.showinfo("Eventos", "Nenhum evento cadastrado.")

def buscar_eventos_interface():
    palavra_chave = entrada_busca.get()
    eventos = buscar_eventos(palavra_chave)
    if eventos:
        eventos_texto = "\n".join([f"{evento[1]} - {evento[2]} em {evento[3]}" for evento in eventos])
        messagebox.showinfo("Resultados da Busca", eventos_texto)
    else:
        messagebox.showinfo("Resultados da Busca", "Nenhum evento encontrado.")

# Configuração da Interface Gráfica
app = tk.Tk()
app.title("Sistema de Anúncio de Eventos Acadêmicos")

# Adicionando padding e espaçamento
app.configure(padx=20, pady=20)

# Seções da Interface
tk.Label(app, text="Título", font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=(0, 5))
entrada_titulo = tk.Entry(app, width=40, font=("Arial", 12))
entrada_titulo.grid(row=1, column=0, pady=(0, 10))

tk.Label(app, text="Descrição", font=("Arial", 12)).grid(row=2, column=0, sticky="w", pady=(0, 5))
entrada_descricao = tk.Entry(app, width=40, font=("Arial", 12))
entrada_descricao.grid(row=3, column=0, pady=(0, 10))

tk.Label(app, text="Data (DD/MM/AAAA)", font=("Arial", 12)).grid(row=4, column=0, sticky="w", pady=(0, 5))
entrada_data = tk.Entry(app, width=40, font=("Arial", 12))
entrada_data.grid(row=5, column=0, pady=(0, 20))

tk.Button(app, text="Adicionar Evento", command=adicionar_evento_interface, font=("Arial", 12)).grid(row=6, column=0, pady=(0, 10))
tk.Button(app, text="Mostrar Eventos", command=mostrar_eventos_interface, font=("Arial", 12)).grid(row=7, column=0, pady=(0, 10))

tk.Label(app, text="Buscar Eventos", font=("Arial", 12)).grid(row=8, column=0, sticky="w", pady=(0, 5))
entrada_busca = tk.Entry(app, width=40, font=("Arial", 12))
entrada_busca.grid(row=9, column=0, pady=(0, 10))

tk.Button(app, text="Buscar", command=buscar_eventos_interface, font=("Arial", 12)).grid(row=10, column=0, pady=(0, 20))

# Criar Banco de Dados ao iniciar
criar_banco_dados()

# Executar Aplicação
app.mainloop()