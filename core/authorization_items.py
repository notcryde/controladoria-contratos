import streamlit as st
import pandas as pd
import logging

from database.connection import get_connection

def get_all(auth_number: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        query = 'SELECT * FROM authorization_items WHERE authorization_number = ?'
        df = pd.read_sql_query(query, conn, params=(auth_number,))
        return df
    except Exception as e:
        logging.error(f'Erro ao carregar itens da autorização {auth_number}: {e}')
        return pd.DataFrame()
    finally:
        conn.close()

def get_by_auth_number(auth_number: str) -> list:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, material_code FROM authorization_items WHERE authorization_number = ?', (auth_number,))
        rows = cursor.fetchall()
        return [{'id': row['id'], 'material_code': row['material_code']} for row in rows]
    finally:
        conn.close()

def get_by_id(item_id: int) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authorization_items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def update(item_id: int, data: dict) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE authorization_items
            SET description = ?, quantity = ?, unitary_value = ?
            WHERE id = ?
        ''', (data['description'], data['quantity'], data['unitary_value'], item_id))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f'Erro ao atualizar item da autorização: {e}')
        st.error('Erro interno ao atualizar os dados.')
        return False
    finally:
        conn.close()
