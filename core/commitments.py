import streamlit as st
import pandas as pd
import sqlite3
import logging
from database.connection import get_connection
from utils.formatters import parse_currency

def get_available_requests(req_type: str) -> list:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        query = '''
            SELECT r.request_number 
            FROM requests r
            LEFT JOIN commitments c ON r.request_number = c.request_number
            WHERE r.request_type = ? AND c.request_number IS NULL
        '''
        cursor.execute(query, (req_type,))
        rows = cursor.fetchall()
        return [row['request_number'] for row in rows]
    except Exception as e:
        logging.error(f'Erro ao buscar solicitações disponíveis: {e}')
        return []
    finally:
        conn.close()

def insert(extracted_data: dict, selected_request: str) -> bool:
    commitment_number = extracted_data.get('commitment_number')
    if not commitment_number:
        st.error('Número do empenho não encontrado no documento.')
        return False

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO commitments 
            (commitment_number, request_number, commited_value, process_number, 
             source, supplier_name, supplier_cnpj, supplier_phone, supplier_email)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            commitment_number,
            selected_request,
            parse_currency(extracted_data.get('commited_value')),
            extracted_data.get('process_number'),
            extracted_data.get('source'),
            extracted_data.get('supplier_name'),
            extracted_data.get('supplier_cnpj'),
            extracted_data.get('supplier_phone'),
            extracted_data.get('supplier_email')
        ))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error(f'Erro de integridade: O empenho {commitment_number} ou a solicitação {selected_request} já possui vínculo cadastrado.')
        return False
    except Exception as e:
        logging.error(f'Erro ao inserir empenho: {e}')
        st.error('Erro interno ao processar o banco de dados.')
        return False
    finally:
        conn.close()

def get_all() -> pd.DataFrame:
    conn = get_connection()
    try:
        query = 'SELECT * FROM commitments'
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        logging.error(f'Erro ao carregar empenhos: {e}')
        return pd.DataFrame()
    finally:
        conn.close()

def get_by_id(commitment_number: str) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM commitments WHERE commitment_number = ?', (commitment_number,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def update(commitment_number: str, data: dict) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE commitments
            SET commited_value = ?, process_number = ?, source = ?,
                supplier_name = ?, supplier_cnpj = ?, supplier_phone = ?, supplier_email = ?
            WHERE commitment_number = ?
        ''', (
            data['commited_value'], data['process_number'], data['source'],
            data['supplier_name'], data['supplier_cnpj'], data['supplier_phone'], data['supplier_email'],
            commitment_number
        ))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f'Erro ao atualizar empenho: {e}')
        st.error('Erro interno ao atualizar os dados.')
        return False
    finally:
        conn.close()
