import streamlit as st
import pandas as pd
import sqlite3
import logging
from database.connection import get_connection
from core.pdf_extractor import extract_text_from_pdf, extract_data, extract_items
from core.regex_patterns import INVOICES, INVOICE_ITEMS
from core.formatters import format_date_to_database, parse_currency

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
        saldo_inicial = row_init[0] if row_init and row_init[0] else 0.0
        
        cursor.execute('''
            SELECT SUM(ii.quantity * ii.unitary_value) 
            FROM invoice_items ii 
            JOIN invoices i ON ii.invoice_number = i.invoice_number 
            WHERE i.authorization_number = ?
        ''', (auth_number,))
        row_exec = cursor.fetchone()
        saldo_executado = row_exec[0] if row_exec and row_exec[0] else 0.0
        
        saldo_atual = saldo_inicial - saldo_executado
        
        if new_invoice_total > saldo_atual:
            st.error(f'NF {inv_number}: A operação foi bloqueada. O valor (R$ {new_invoice_total:.2f}) ultrapassa o saldo atual da AF (R$ {saldo_atual:.2f}).')
            return False
        return True
    finally:
        conn.close()

def insert_invoice(inv_data: dict, items_data: list) -> bool:
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
            (invoice_number, authorization_number, issue_date, executed_value)
            VALUES (?, ?, ?, ?)
        ''', (
            inv_number,
            auth_number,
            format_date_to_database(inv_data.get('issue_date')),
            parse_currency(inv_data.get('executed_value'))
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

def load_invoices() -> pd.DataFrame:
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

def load_invoice_items(inv_number: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        query = 'SELECT * FROM invoice_items WHERE invoice_number = ?'
        df = pd.read_sql_query(query, conn, params=(inv_number,))
        return df
    except Exception as e:
        logging.error(f'Erro ao carregar itens da NF {inv_number}: {e}')
        return pd.DataFrame()
    finally:
        conn.close()

def get_invoice(inv_number: str) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM invoices WHERE invoice_number = ?', (inv_number,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def update_invoice(inv_number: str, data: dict) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE invoices
            SET issue_date = ?, executed_value = ?
            WHERE invoice_number = ?
        ''', (data['issue_date'], data['executed_value'], inv_number))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f'Erro ao atualizar nota fiscal: {e}')
        st.error('Os dados apresentaram um erro interno durante a atualização.')
        return False
    finally:
        conn.close()

def get_inv_items_for_select(inv_number: str) -> list:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, material_code FROM invoice_items WHERE invoice_number = ?', (inv_number,))
        rows = cursor.fetchall()
        return [{'id': row['id'], 'material_code': row['material_code']} for row in rows]
    finally:
        conn.close()

def get_invoice_item_by_id(item_id: int) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM invoice_items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def update_invoice_item(item_id: int, data: dict) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE invoice_items
            SET description = ?, quantity = ?, unitary_value = ?
            WHERE id = ?
        ''', (data['description'], data['quantity'], data['unitary_value'], item_id))
        conn.commit()
        return True
    except Exception as e:
        logging.error(f'Erro ao atualizar item da nota fiscal: {e}')
        st.error('Os dados apresentaram um erro interno durante a atualização.')
        return False
    finally:
        conn.close()

def render():
    st.header('Gestão de Notas Fiscais')
    
    df_invoices = load_invoices()
    has_data = not df_invoices.empty
    
    with st.expander('Processar Novas Notas Fiscais', expanded=True):
        uploaded_files = st.file_uploader(
            'Faça o upload das notas fiscais (PDF)', 
            type=['pdf'],
            accept_multiple_files=True,
            key='invoice_upload'
        )
            
        if st.button('Processar', type='primary', key='btn_process_invoices'):
            if uploaded_files:
                with st.spinner(f'Extraindo dados de {len(uploaded_files)} documento(s)...'):
                    for uploaded_file in uploaded_files:
                        pdf_text = extract_text_from_pdf(uploaded_file)
                        
                        if not pdf_text.strip():
                            st.error(f'O texto do documento {uploaded_file.name} não foi extraído.')
                            continue
                        
                        inv_data = extract_data(pdf_text, INVOICES)
                        items_data = extract_items(pdf_text, INVOICE_ITEMS)
                        inv_number = inv_data.get('invoice_number', uploaded_file.name)
                        
                        if not items_data:
                            st.warning(f'NF {inv_number}: A captura detectou a NF, mas os itens formatados corretamente não foram identificados.')
                        
                        if insert_invoice(inv_data, items_data):
                            st.success(f'NF {inv_number}: A nota e os itens vinculados foram processados com sucesso!')
                    
                    st.rerun()
            else:
                st.warning('Selecione pelo menos um arquivo PDF antes de processar.')

    with st.expander('Editar Dados', expanded=False):
        if not has_data:
            st.info('As notas fiscais não estão cadastradas no sistema.')
        else:
            options = df_invoices['invoice_number'].tolist()
            selected_edit = st.selectbox('Número da Nota Fiscal', options, key='edit_inv_num')
            
            if selected_edit:
                inv_data = get_invoice(selected_edit)
                if inv_data:
                    with st.form(f'form_edit_{selected_edit}'):
                        st.markdown(f'**Editando Nota Fiscal: {selected_edit}**')
                        
                        i_date = st.text_input('Data de Emissão (YYYY-MM-DD)', value=inv_data.get('issue_date') or '')
                        e_val = st.number_input('Valor Executado (R$)', value=float(inv_data.get('executed_value') or 0.0), step=0.01)
                        
                        submitted = st.form_submit_button('Salvar Alterações', key='btn_submit_invoice')
                        if submitted:
                            new_data = {
                                'issue_date': i_date,
                                'executed_value': e_val
                            }
                            if update_invoice(selected_edit, new_data):
                                st.success('Os dados foram atualizados com sucesso!')
                                st.rerun()

    with st.expander('Editar Item', expanded=False):
        if not has_data:
            st.info('As notas fiscais não estão cadastradas no sistema.')
        else:
            options = df_invoices['invoice_number'].tolist()
            selected_inv_item = st.selectbox('Número da Nota Fiscal', options, key='edit_item_inv_num')
            
            if selected_inv_item:
                items_for_select = get_inv_items_for_select(selected_inv_item)
                if not items_for_select:
                    st.info('Os itens vinculados a esta Nota Fiscal não existem.')
                else:
                    selected_item_dict = st.selectbox(
                        'Código Material', 
                        items_for_select, 
                        format_func=lambda x: x['material_code'],
                        key='slb_item_mat_code'
                    )
                    
                    if selected_item_dict:
                        item_id = selected_item_dict['id']
                        item_data = get_invoice_item_by_id(item_id)
                        
                        if item_data:
                            with st.form(key='form'):
                                st.markdown(f'**Editando Item: {item_data["material_code"]}**')
                                
                                desc = st.text_area('Descrição', value=item_data.get('description') or '')
                                qty = st.number_input('Quantidade', value=float(item_data.get('quantity') or 0.0), step=0.01)
                                val = st.number_input('Valor Unitário (R$)', value=float(item_data.get('unitary_value') or 0.0), step=0.01)
                                
                                submitted_item = st.form_submit_button('Salvar Alterações', key='btn_submit_item_invoice')
                                if submitted_item:
                                    new_item_data = {
                                        'description': desc,
                                        'quantity': qty,
                                        'unitary_value': val
                                    }
                                    if update_invoice_item(item_id, new_item_data):
                                        st.success('O item foi atualizado com sucesso!')
                                        st.rerun()

    st.markdown('---')
    
    st.subheader('Notas Fiscais Processadas')
    
    tab_inv, tab_items = st.tabs(['Notas Fiscais', 'Itens de NF'])
    
    with tab_inv:
        if not df_invoices.empty:
            st.dataframe(df_invoices, use_container_width=True, hide_index=True)
        else:
            st.info('A Nota Fiscal não está cadastrada.')
            
    with tab_items:
        if not df_invoices.empty:
            inv_list = df_invoices['invoice_number'].tolist()
            selected_inv = st.selectbox(
                'Selecione o número da Nota Fiscal', 
                inv_list,
                key='select_inv_items'
            )
            
            if selected_inv:
                df_items = load_invoice_items(selected_inv)
                if not df_items.empty:
                    st.dataframe(df_items, use_container_width=True, hide_index=True)
                else:
                    st.info('Nenhum item foi encontrado para esta Nota Fiscal.')
        else:
            st.info('As Notas Fiscais não estão cadastradas para exibir itens.')