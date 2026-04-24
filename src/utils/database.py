import sqlite3
import pandas as pd

from src.utils.constants import (
    SOLIC_COMP_TABLE, SOLIC_CONS_TABLE, EMPENHOS_TABLE, 
    AF_TABLE, NF_TABLE, NF_ITENS_TABLE, AF_ITENS_TABLE
)

def get_database_connection():
    return sqlite3.connect('controladoria.db', check_same_thread=False)

def initialize_database():
    connection = get_database_connection()
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute(SOLIC_COMP_TABLE)
    cursor.execute(SOLIC_CONS_TABLE)
    cursor.execute(EMPENHOS_TABLE)
    cursor.execute(AF_TABLE)
    cursor.execute(NF_TABLE)
    cursor.execute(NF_ITENS_TABLE)
    cursor.execute(AF_ITENS_TABLE)
    

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

def save_items_notas_fiscais(items_list):
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

def save_autorizacoes_fornecimento_items(items_list):
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
    dataframe.to_sql('autorizacoes_itens', connection, if_exists='append', index=False)
    connection.close()

def load_data(table_name):
    connection = get_database_connection()
    try:
        dataframe = pd.read_sql(f'SELECT * FROM {table_name}', connection)
    except:
        dataframe = pd.DataFrame()
    connection.close()
    return dataframe

def load_items_notas_fiscais(numero_nf):
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