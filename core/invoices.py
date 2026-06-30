import streamlit as st
import pandas as pd
import sqlite3
import logging
from database.connection import get_connection
from utils.formatters import format_date_to_database, parse_currency

def check_authorization_exists(auth_number: str) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM authorizations WHERE authorization_number = ?', (auth_number,))
        return cursor.fetchone() is not None
    finally:
        conn.close()

def check_balance_before_insert(auth_number: str, new_invoice_total: float, inv_number: str) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT SUM(quantity * unitary_value) 
            FROM authorization_items 
            WHERE authorization_number = ?
        ''', (auth_number,))
        row_init = cursor.fetchone()
        opening_balance = row_init[0] if row_init and row_init[0] else 0.0
        
        cursor.execute('''
            SELECT SUM(ii.quantity * ii.unitary_value) 
            FROM invoice_items ii 
            JOIN invoices i ON ii.invoice_number = i.invoice_number 
            WHERE i.authorization_number = ?
        ''', (auth_number,))
        row_exec = cursor.fetchone()
        executed_balance = row_exec[0] if row_exec and row_exec[0] else 0.0
        
        current_balance = opening_balance - executed_balance
        
        if new_invoice_total > current_balance:
            st.error(f'NF {inv_number}: A operação foi bloqueada. O valor (R$ {new_invoice_total:.2f}) ultrapassa o saldo atual da AF (R$ {current_balance:.2f}).')
            return False
        return True
    finally:
        conn.close()

def insert(inv_data: dict, items_data: list) -> bool:
    inv_number = inv_data.get('invoice_number')
    auth_number = inv_data.get('authorization_number')
    
    if not inv_number:
        st.error('O número da nota fiscal não foi encontrado em um dos documentos.')
        return False
        
    if not auth_number:
        st.error(f'NF {inv_number}: O número da autorização não foi encontrado no documento.')
        return False

    if not check_authorization_exists(auth_number):
        st.error(f'NF {inv_number}: A autorização {auth_number} não está cadastrada no sistema.')
        return False

    new_total = sum([parse_currency(item.get('quantity')) * parse_currency(item.get('unitary_value')) for item in items_data])
    
    if not check_balance_before_insert(auth_number, new_total, inv_number):
        return False

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO invoices 
            (invoice_number, authorization_number, issue_date)
            VALUES (?, ?, ?)
        ''', (
            inv_number,
            auth_number,
            format_date_to_database(inv_data.get('issue_date')),
        ))
        
        for item in items_data:
            cursor.execute('''
                INSERT INTO invoice_items 
                (invoice_number, material_code, description, quantity, unitary_value)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                inv_number,
                item.get('material_code'),
                item.get('descriptions'), 
                parse_currency(item.get('quantity')),
                parse_currency(item.get('unitary_value'))
            ))
            
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error(f'NF {inv_number}: A Nota Fiscal já está cadastrada (Erro de integridade).')
        return False
    except Exception as e:
        logging.error(f'Erro ao inserir nota fiscal {inv_number}: {e}')
        st.error(f'NF {inv_number}: O banco de dados apresentou um erro interno.')
        return False
    finally:
        conn.close()

def get_all() -> pd.DataFrame:
    conn = get_connection()
    try:
        query = 'SELECT * FROM invoices'
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        logging.error(f'Erro ao carregar notas fiscais: {e}')
        return pd.DataFrame()
    finally:
        conn.close()

def get_by_id(inv_number: str) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM invoices WHERE invoice_number = ?', (inv_number,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def update(inv_number: str, data: dict) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE invoices
            SET issue_date = ?
            WHERE invoice_number = ?
        ''', (data['issue_date'], inv_number))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f'Erro ao atualizar nota fiscal: {e}')
        st.error('Os dados apresentaram um erro interno durante a atualização.')
        return False
    finally:
        conn.close()
