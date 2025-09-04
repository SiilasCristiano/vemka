import sqlite3

# Conexão com o banco
conn = sqlite3.connect("vemka.db", check_same_thread=False)
cursor = conn.cursor()

# Criar a tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,         -- casal, solteiro, solteira
    email TEXT UNIQUE,
    senha TEXT,
    nome TEXT,
    idade INTEGER,
    bio TEXT
)
''')

# Adicionar colunas de fotos se não existirem
colunas_fotos = ['foto1', 'foto2', 'foto3', 'foto4']
for coluna in colunas_fotos:
    try:
        cursor.execute(f"ALTER TABLE usuarios ADD COLUMN {coluna} TEXT")
    except sqlite3.OperationalError:
        # Coluna já existe
        pass

conn.commit()
conn.close()
