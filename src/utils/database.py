import sqlite3
import pandas as pd

def get_database_connection():
    return sqlite3.connect('dados.db', check_same_thread=False)

def initialize_database():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes_consumo (
            "Nº Solicitação" TEXT PRIMARY KEY,
            "Nº Processo" TEXT,
            "Data Emissão" TEXT,
            "Valor Solicitado" REAL,
            "Ata RP" TEXT,
            "Vigência Inicial" TEXT,
            "Vigência Final" TEXT,
            "Status" TEXT,
            "Prazo Exec." TEXT,
            "Forma Exec." TEXT,
            "Local Entrega" TEXT,
            "Funcionário" TEXT,
            "Unidade Solicitante" TEXT,
            "Órgão Financeiro" TEXT,
            "Unidade Financeira" TEXT,
            "Observação" TEXT,
            "Nome do Fornecedor" TEXT,
            "CNPJ do Fornecedor" TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS solicitacoes_compras (
            "Nº Solicitação" TEXT PRIMARY KEY,
            "Nº Processo" TEXT,
            "Data Emissão" TEXT,
            "Valor Solicitado" REAL,
            "Local Entrega" TEXT,
            "Objeto" TEXT,
            "Observação" TEXT,
            "Status" TEXT,
            "Prazo Exec." TEXT,
            "Forma Exec." TEXT,
            "Funcionário" TEXT,
            "Órgão Financeiro" TEXT,
            "Unidade Solicitante" TEXT,
            "Unidade Financeira" TEXT,
            "Ação" TEXT,
            "Gestor Indicado" TEXT,
            "Legislação" TEXT,
            "Programa" TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS empenhos (
            "Nº Empenho" TEXT PRIMARY KEY,
            "Nº Processo" TEXT,
            "Nº Solicitação" TEXT,
            "Valor Empenhado" REAL,
            "Órgão Solicitante" TEXT,
            "Unidade" TEXT,
            "Ação" TEXT,
            "Fonte" TEXT,
            "Nome Fornecedor" TEXT,
            "CNPJ Fornecedor" TEXT,
            "Tel. Fornecedor" TEXT,
            "E-mail Fornecedor" TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS autorizacoes (
            "Nº AF" TEXT PRIMARY KEY,
            "Nº Empenho" TEXT,
            "Data" TEXT,
            "Valor Empenhado" REAL,
            "Vigência Inicial" TEXT,
            "Vigência Final" TEXT,
            "Nº Processo" TEXT,
            "Fonte de Recurso" TEXT,
            "Objeto" TEXT,
            "Ano Processo" TEXT,
            "Nº Modalidade" TEXT,
            "Ano Modalidade" TEXT,
            "Modalidade" TEXT,
            "Contrato/Ano" TEXT,
            "Valor Contrato" REAL,
            "Prazo de Entrega" TEXT,
            "Local de Entrega" TEXT,
            "Prazo de Pagamento" TEXT,
            "Observacoes" TEXT,
            "Total Liberação" REAL,
            "Solicitacoes de Compra" TEXT,
            "Solicitacoes de Consumo" TEXT,
            "Órgão Solicitante" TEXT,
            "Ficha" TEXT,
            "Dotacao" TEXT,
            "Nº Fornecedor" TEXT,
            "Nome Fornecedor" TEXT,
            "CNPJ" TEXT,
            "Fone" TEXT,
            "Email" TEXT,
            "Contas" TEXT,
            FOREIGN KEY ("Nº Empenho") REFERENCES empenhos ("Nº Empenho")
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas_fiscais (
            "Nº NF" TEXT PRIMARY KEY,
            "Nº AF" TEXT,
            "Nº Empenho" TEXT,
            "Data Emissão" TEXT,
            "Valor Executado" REAL,
            "Fornecedor" TEXT,
            FOREIGN KEY ("Nº AF") REFERENCES autorizacoes ("Nº AF"),
            FOREIGN KEY ("Nº Empenho") REFERENCES empenhos ("Nº Empenho")
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notas_fiscais_itens (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT,
            "Nº NF" TEXT,
            "Cód. Material" TEXT,
            "Descrição" TEXT,
            "Qtde" REAL,
            "Vlr. Unitário" REAL,
            "Valor Executado" REAL,
            FOREIGN KEY ("Nº NF") REFERENCES notas_fiscais ("Nº NF")
        )
    ''')

    connection.commit()
    connection.close()

def save_document(table_name, document_data):
    connection = get_database_connection()
    connection.execute('PRAGMA foreign_keys = ON')
    
    for key, value in document_data.items():
        if isinstance(value, str) and ('Valor' in key or 'Total' in key or 'Liberação' in key or 'Qtde' in key):
            try:
                document_data[key] = float(value.replace('.', '').replace(',', '.'))
            except ValueError:
                pass

    dataframe = pd.DataFrame([document_data])
    dataframe.to_sql(table_name, connection, if_exists='append', index=False)
    connection.close()

def save_nf_items(items_list):
    if not items_list:
        return
        
    connection = get_database_connection()
    connection.execute('PRAGMA foreign_keys = ON')
    
    for item in items_list:
        for key, value in item.items():
            if isinstance(value, str) and ('Vlr.' in key or 'Qtde' in key or 'Valor' in key):
                try:
                    item[key] = float(value.replace('.', '').replace(',', '.'))
                except ValueError:
                    pass
                    
    dataframe = pd.DataFrame(items_list)
    dataframe.to_sql('notas_fiscais_itens', connection, if_exists='append', index=False)
    connection.close()

def load_data(table_name):
    connection = get_database_connection()
    try:
        dataframe = pd.read_sql(f'SELECT * FROM {table_name}', connection)
    except:
        dataframe = pd.DataFrame()
    connection.close()
    return dataframe

def load_nf_items(numero_nf):
    connection = get_database_connection()
    try:
        dataframe = pd.read_sql(f'SELECT "Cód. Material", "Descrição", "Qtde", "Vlr. Unitário", "Valor Executado" FROM notas_fiscais_itens WHERE "Nº NF" = ?', connection, params=(numero_nf,))
    except:
        dataframe = pd.DataFrame()
    connection.close()
    return dataframe

def get_solicitacoes_por_tipo(tipo_solicitacao):
    table_name = 'solicitacoes_compras' if tipo_solicitacao == 'Compras' else 'solicitacoes_consumo'
    connection = get_database_connection()
    try:
        dataframe = pd.read_sql(f'SELECT "Nº Solicitação" FROM {table_name}', connection)
        lista_solicitacoes = dataframe['Nº Solicitação'].dropna().unique().tolist()
    except:
        lista_solicitacoes = []
    connection.close()
    return lista_solicitacoes