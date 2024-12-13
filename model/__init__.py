from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Importando os elementos definidos no modelo
from model.base import Base
from model.usuario import Usuario
from model.moeda import Moeda

db_path = "database/"
# Verifica se o diretório não existe
if not os.path.exists(db_path):
    # então cria o diretório
    os.makedirs(db_path)

# URL de acesso ao banco (essa é uma URL de acesso ao SQLite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de sessão com o banco
Session = sessionmaker(bind=engine)

# Cria o banco se ele não existir
if not database_exists(engine.url):
    create_database(engine.url)

# Cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)

# Insere o usuário inicial, caso não exista
session = Session()  # Cria uma sessão para interagir com o banco

# Verifica se já existe um usuário na tabela
usuario_existente = session.query(Usuario).first()

if not usuario_existente:
    # Cria o usuário padrão
    usuario_padrao = Usuario()
    session.add(usuario_padrao)
    session.commit()
    print("Usuário inicial criado com sucesso!")

# Fecha a sessão
session.close()