import sqlite3

# Inicializa o banco de dados SQLite
def init_db():
    conn = sqlite3.connect("procon_chatbot.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS reclamacoes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        cpf TEXT,
                        email TEXT,
                        data_nascimento TEXT,
                        telefone TEXT,
                        endereco TEXT,
                        produto TEXT,
                        nota_fiscal TEXT,
                        documento BLOB,
                        descricao TEXT)''')
    conn.commit()
    conn.close()

# Função para salvar a reclamação no banco de dados
def salvar_reclamacao(dados):
    conn = sqlite3.connect("procon_chatbot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reclamacoes (nome, cpf, email, data_nascimento, telefone, endereco, produto, nota_fiscal, documento, descricao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dados)
    conn.commit()
    conn.close()

# Inicializa o banco de dados ao importar este módulo
init_db()
