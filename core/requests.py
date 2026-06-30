import streamlit as st
import pandas as pd
import sqlite3
import logging
from database.connection import get_connection
from utils.formatters import format_date_to_database, parse_currency


def insert(request_type: str, extracted_data: dict) -> bool:
    request_number = extracted_data.get('request_number')
    if not request_number:
        st.error('Número da solicitação não encontrado no documento.')
        return False

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO requests (request_number, request_type) VALUES (?, ?)', 
            (request_number, request_type)
        )
        
        if request_type == 'Consumo':
            cursor.execute('''
                INSERT INTO consumption_requests 
                (request_number, requested_value, price_registration, start_date, end_date, 
                 requesting_unit, financial_department, notes, supplier_name, supplier_cnpj)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request_number,
                parse_currency(extracted_data.get('requested_value')),
                extracted_data.get('price_registration'),
                format_date_to_database(extracted_data.get('start_date')),
                format_date_to_database(extracted_data.get('end_date')),
                extracted_data.get('requesting_unit'),
                extracted_data.get('financial_department'),
                extracted_data.get('notes'),
                extracted_data.get('supplier_name'),
                extracted_data.get('supplier_cnpj')
            ))
        else:
            cursor.execute('''
                INSERT INTO purchase_requests 
                (request_number, issue_date, requested_value, object, notes, 
                 requesting_unit, financial_department, activity, designed_manager, legislation, program)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                request_number,
                format_date_to_database(extracted_data.get('issue_date')),
                parse_currency(extracted_data.get('requested_value')),
                extracted_data.get('object'),
                extracted_data.get('notes'),
                extracted_data.get('requesting_unit'),
                extracted_data.get('financial_department'),
                extracted_data.get('activity'),
                extracted_data.get('designed_manager'),
                extracted_data.get('legislation'),
                extracted_data.get('program')
            ))
            
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        st.error(f'A solicitação {request_number} já está cadastrada no sistema.')
        return False
    except Exception as e:
        logging.error(f'Erro ao inserir solicitação: {e}')
        st.error('Erro interno ao processar o banco de dados.')
        return False
    finally:
        conn.close()

def get_all(table_name: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        query = f'SELECT * FROM {table_name}'
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        logging.error(f'Erro ao carregar dados da tabela {table_name}: {e}')
        return pd.DataFrame()
    finally:
        conn.close()

def get_by_id(request_number: str, request_type: str) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        table = 'consumption_requests' if request_type == 'Consumo' else 'purchase_requests'
        cursor.execute(f'SELECT * FROM {table} WHERE request_number = ?', (request_number,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def update(request_number: str, request_type: str, data: dict) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if request_type == 'Consumo':
            cursor.execute('''
                UPDATE consumption_requests
                SET requested_value = ?, price_registration = ?, start_date = ?, end_date = ?,
                    requesting_unit = ?, financial_department = ?, notes = ?, supplier_name = ?, supplier_cnpj = ?
                WHERE request_number = ?
            ''', (
                data['requested_value'], data['price_registration'], data['start_date'], data['end_date'],
                data['requesting_unit'], data['financial_department'], data['notes'], data['supplier_name'], data['supplier_cnpj'],
                request_number
            ))
        else:
            cursor.execute('''
                UPDATE purchase_requests
                SET issue_date = ?, requested_value = ?, object = ?, notes = ?,
                    requesting_unit = ?, financial_department = ?, activity = ?, designed_manager = ?, legislation = ?, program = ?
                WHERE request_number = ?
            ''', (
                data['issue_date'], data['requested_value'], data['object'], data['notes'],
                data['requesting_unit'], data['financial_department'], data['activity'], data['designed_manager'], data['legislation'], data['program'],
                request_number
            ))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f'Erro ao atualizar solicitação: {e}')
        st.error('Erro interno ao atualizar os dados.')
        return False
    finally:
        conn.close()
