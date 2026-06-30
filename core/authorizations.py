import streamlit as st
import pandas as pd
import sqlite3
import logging

from utils.formatters import parse_currency
from database.connection import get_connection

def check_commitment_exists(commitment_number: str) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM commitments WHERE commitment_number = ?', (commitment_number,))
        return cursor.fetchone() is not None
    finally:
        conn.close()

def insert(auth_data: dict, items_data: list, start_date, end_date) -> bool:
    auth_number = auth_data.get('authorization_number')
    commit_number = auth_data.get('commitment_number')
    
    if not auth_number:
        st.error('O número da autorização não foi encontrado no documento.')
        return False
        
    if not commit_number:
        st.error('O número do empenho não foi encontrado no documento.')
        return False

    if not check_commitment_exists(commit_number):
        st.error(f'O empenho {commit_number} não está cadastrado no sistema. Efetue o processamento do empenho primeiro.')
        return False

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO authorizations 
            (authorization_number, commitment_number, process_number, modality, 
             contract, notes, budget_sheet, budget_allocation, start_date, end_date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            auth_number,
            commit_number,
            auth_data.get('process_number'),
            auth_data.get('modality'),
            auth_data.get('contract'),
            auth_data.get('notes'),
            auth_data.get('budget_sheet'),
            auth_data.get('budget_allocation'),
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        ))
        
        for item in items_data:
            cursor.execute('''
                INSERT INTO authorization_items 
                (authorization_number, material_code, description, quantity, unitary_value)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                auth_number,
                item.get('material_code'),
                item.get('description'),
                parse_currency(item.get('qquantity')), 
                parse_currency(item.get('unitary_value'))
            ))
            
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error(f'Erro de integridade: A autorização {auth_number} ou o vínculo com o empenho {commit_number} já existe.')
        return False
    except Exception as e:
        logging.error(f'Erro ao inserir autorização: {e}')
        st.error('Erro interno ao processar o banco de dados.')
        return False
    finally:
        conn.close()

def get_all() -> pd.DataFrame:
    conn = get_connection()
    try:
        query = 'SELECT * FROM authorizations'
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        logging.error(f'Erro ao carregar autorizações: {e}')
        return pd.DataFrame()
    finally:
        conn.close()

def update(auth_number: str, data: dict) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE authorizations
            SET process_number = ?, modality = ?, contract = ?, notes = ?,
                budget_sheet = ?, budget_allocation = ?, start_date = ?, end_date = ?
            WHERE authorization_number = ?
        ''', (
            data['process_number'], data['modality'], data['contract'], data['notes'],
            data['budget_sheet'], data['budget_allocation'], data['start_date'], data['end_date'],
            auth_number
        ))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f'Erro ao atualizar autorização: {e}')
        st.error('Erro interno ao atualizar os dados.')
        return False
    finally:
        conn.close()

def get_by_id(auth_number: str) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authorizations WHERE authorization_number = ?', (auth_number,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()