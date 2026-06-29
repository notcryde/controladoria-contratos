import sqlite3
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

DB_DIR = Path(__file__).parent
DB_PATH = DB_DIR / 'database.db'
SCHEMA_PATH = DB_DIR / 'schema.sql'

def get_connection() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row 
        conn.execute('PRAGMA foreign_keys = ON;')
        return conn
    except sqlite3.Error as e:
        logging.error(f'Erro ao conectar ao banco de dados: {e}')
        raise

def init_db():
    '''Lê o arquivo schema.sql e constrói as tabelas caso não existam.'''
    if not SCHEMA_PATH.exists():
        logging.error('Arquivo schema.sql não localizado no diretório /database.')
        return

    try:
        with get_connection() as conn:
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                schema_script = f.read()
            
            conn.executescript(schema_script)
            logging.info('Estrutura do banco de dados verificada/inicializada com sucesso.')
    except sqlite3.Error as e:
        logging.error(f'Erro na execução do script SQL: {e}')
        raise
    except Exception as e:
        logging.error(f'Erro inesperado ao inicializar banco: {e}')
        raise