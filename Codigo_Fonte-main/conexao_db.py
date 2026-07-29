from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

# 1. Carrega o arquivo .env
load_dotenv()

# 2. Pega a URL do banco
endereco_banco = os.getenv('DATABASE_URL')

# 3. Cria o motor de conexão (o switchzinho)
engine = create_engine(endereco_banco)

print("Conexão configurada com sucesso!")