import streamlit as st
import pandas as pd
import sqlite3
import logging
from database.connection import get_connection
from core.pdf_extractor import extract_text_from_pdf, extract_data, extract_items
from core.regex_patterns import AUTHORIZATIONS, AUTHORIZATION_ITEMS
from core.formatters import parse_currency

def check_commitment_exists(commitment_number: str) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM commitments WHERE commitment_number = ?', (commitment_number,))
        return cursor.fetchone() is not None
    finally:
        conn.close()

def insert_authorization(auth_data: dict, items_data: list, start_date, end_date) -> bool:
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

def load_authorizations() -> pd.DataFrame:
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

def load_authorization_items(auth_number: str) -> pd.DataFrame:
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

def get_authorization(auth_number: str) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authorizations WHERE authorization_number = ?', (auth_number,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def update_authorization(auth_number: str, data: dict) -> bool:
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

def get_auth_items_for_select(auth_number: str) -> list:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT id, material_code FROM authorization_items WHERE authorization_number = ?', (auth_number,))
        rows = cursor.fetchall()
        return [{'id': row['id'], 'material_code': row['material_code']} for row in rows]
    finally:
        conn.close()

def get_authorization_item_by_id(item_id: int) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authorization_items WHERE id = ?', (item_id,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def update_authorization_item(item_id: int, data: dict) -> bool:
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

def render():
    st.header('Gestão de Autorizações de Fornecimento')
    
    df_authorizations = load_authorizations()
    has_data = not df_authorizations.empty

    with st.expander('Processar Nova Autorização', expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input('Selecione a data inicial', format='DD/MM/YYYY')
            end_date = st.date_input('Selecione a data final', format='DD/MM/YYYY')
            
        with col2:
            uploaded_file = st.file_uploader(
                'Faça o upload da autorização (PDF)', 
                type=['pdf'],
                key='auth_upload'
            )
            
        if st.button('Processar', type='primary'):
            if uploaded_file is not None:
                if start_date > end_date:
                    st.error('A data inicial não pode ser posterior à data final.')
                else:
                    with st.spinner('Extraindo dados da autorização...'):
                        pdf_text = extract_text_from_pdf(uploaded_file)
                        
                        if not pdf_text.strip():
                            st.error('O texto do documento não foi extraído.')
                        else:
                            auth_data = extract_data(pdf_text, AUTHORIZATIONS)
                            items_data = extract_items(pdf_text, AUTHORIZATION_ITEMS)
                            
                            if not items_data:
                                st.warning('A captura detectou a autorização, mas os itens formatados corretamente não foram identificados.')
                            
                            if insert_authorization(auth_data, items_data, start_date, end_date):
                                st.success('A autorização e os itens vinculados foram processados com sucesso!')
                                st.rerun()
            else:
                st.warning('Selecione um arquivo PDF antes de processar.')

    with st.expander('Editar Dados', expanded=False):
        if not has_data:
            st.info('As autorizações não estão cadastradas no sistema.')
        else:
            options = df_authorizations['authorization_number'].tolist()
            selected_edit = st.selectbox('Número da Autorização', options, key='edit_auth_num')
            
            if selected_edit:
                auth_data = get_authorization(selected_edit)
                if auth_data:
                    with st.form(f'form_edit_{selected_edit.replace("/", "_")}'):
                        st.markdown(f'**Editando Autorização: {selected_edit}**')
                        
                        proc = st.text_input('Nº Processo', value=auth_data.get('process_number') or '')
                        mod = st.text_input('Modalidade', value=auth_data.get('modality') or '')
                        cont = st.text_input('Contrato / Ano', value=auth_data.get('contract') or '')
                        nts = st.text_area('Observações', value=auth_data.get('notes') or '')
                        sheet = st.text_input('Ficha', value=auth_data.get('budget_sheet') or '')
                        alloc = st.text_input('Dotação', value=auth_data.get('budget_allocation') or '')
                        s_date = st.text_input('Data Inicial (YYYY-MM-DD)', value=auth_data.get('start_date') or '')
                        e_date = st.text_input('Data Final (YYYY-MM-DD)', value=auth_data.get('end_date') or '')
                        
                        submitted = st.form_submit_button('Salvar Alterações')
                        if submitted:
                            new_data = {
                                'process_number': proc,
                                'modality': mod,
                                'contract': cont,
                                'notes': nts,
                                'budget_sheet': sheet,
                                'budget_allocation': alloc,
                                'start_date': s_date,
                                'end_date': e_date
                            }
                            if update_authorization(selected_edit, new_data):
                                st.success('Os dados foram atualizados com sucesso!')
                                st.rerun()

    with st.expander('Editar Item', expanded=False):
        if not has_data:
            st.info('As autorizações não estão cadastradas no sistema.')
        else:
            options = df_authorizations['authorization_number'].tolist()
            selected_auth_item = st.selectbox('Número da Autorização', options, key='edit_item_auth_num')
            
            if selected_auth_item:
                items_for_select = get_auth_items_for_select(selected_auth_item)
                if not items_for_select:
                    st.info('Os itens vinculados a esta Autorização não existem.')
                else:
                    selected_item_dict = st.selectbox(
                        'Código Material', 
                        items_for_select, 
                        format_func=lambda x: x['material_code'],
                        key='edit_item_mat_code'
                    )
                    
                    if selected_item_dict:
                        item_id = selected_item_dict['id']
                        item_data = get_authorization_item_by_id(item_id)
                        
                        if item_data:
                            with st.form(f'form_edit_item_{item_id}'):
                                st.markdown(f'**Editando Item: {item_data["material_code"]}**')
                                
                                desc = st.text_area('Descrição', value=item_data.get('description') or '')
                                qty = st.number_input('Quantidade', value=float(item_data.get('quantity') or 0.0), step=0.01)
                                val = st.number_input('Valor Unitário (R$)', value=float(item_data.get('unitary_value') or 0.0), step=0.01)
                                
                                submitted_item = st.form_submit_button('Salvar Alterações')
                                if submitted_item:
                                    new_item_data = {
                                        'description': desc,
                                        'quantity': qty,
                                        'unitary_value': val
                                    }
                                    if update_authorization_item(item_id, new_item_data):
                                        st.success('O item foi atualizado com sucesso!')
                                        st.rerun()

    st.markdown('---')
    
    st.subheader('Autorizações Processadas')
    
    tab_auth, tab_items = st.tabs(['Autorizações', 'Itens de AF'])
    
    with tab_auth:
        if not df_authorizations.empty:
            st.dataframe(df_authorizations, use_container_width=True, hide_index=True)
        else:
            st.info('A Autorização não está cadastrada.')
            
    with tab_items:
        if not df_authorizations.empty:
            auth_list = df_authorizations['authorization_number'].tolist()
            selected_auth = st.selectbox(
                'Selecione o número da AF', 
                auth_list,
                key='select_auth_items'
            )
            
            if selected_auth:
                df_items = load_authorization_items(selected_auth)
                if not df_items.empty:
                    st.dataframe(df_items, use_container_width=True, hide_index=True)
                else:
                    st.info('Nenhum item foi encontrado para esta Autorização.')
        else:
            st.info('As Autorizações não estão cadastradas para exibir itens.')