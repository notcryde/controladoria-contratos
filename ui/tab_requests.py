import streamlit as st
import pandas as pd
import sqlite3
import logging
from database.connection import get_connection
from core.pdf_extractor import extract_text_from_pdf, extract_data
from core.regex_patterns import CONSUMPTION_REQUESTS, PURCHASE_REQUESTS
from core.formatters import format_date_to_database, parse_currency

def insert_request(request_type: str, extracted_data: dict) -> bool:
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

def load_data(table_name: str) -> pd.DataFrame:
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

def get_request(request_number: str, request_type: str) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        table = 'consumption_requests' if request_type == 'Consumo' else 'purchase_requests'
        cursor.execute(f'SELECT * FROM {table} WHERE request_number = ?', (request_number,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def update_request(request_number: str, request_type: str, data: dict) -> bool:
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

def render():
    st.header('Gestão de Solicitações')
    
    df_consumption = load_data('consumption_requests')
    df_purchase = load_data('purchase_requests')
    has_data = not df_consumption.empty or not df_purchase.empty

    with st.expander('Processar Documento', expanded=True):
        col1, col2 = st.columns([1, 2])
        
        with col1:
            request_type = st.selectbox(
                'Selecione o tipo de solicitação', 
                ['Compras', 'Consumo']
            )
            
        with col2:
            uploaded_file = st.file_uploader(
                'Faça o upload do documento', 
                type=['pdf']
            )
            
        if st.button('Processar', type='primary', key='btn_process_request'):
            if uploaded_file is not None:
                with st.spinner('Extraindo dados do PDF...'):
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    
                    if not pdf_text.strip():
                        st.error('Não foi possível extrair texto do documento.')
                    else:
                        patterns = CONSUMPTION_REQUESTS if request_type == 'Consumo' else PURCHASE_REQUESTS
                        extracted_data = extract_data(pdf_text, patterns)
                        
                        if insert_request(request_type, extracted_data):
                            st.success(f'Solicitação de {request_type} processada e salva com sucesso!')
                            st.rerun()
            else:
                st.warning('Selecione um arquivo PDF antes de processar.')

    with st.expander('Editar Dados', expanded=False):
        if not has_data:
            st.info('Não há solicitações cadastradas no sistema.')
        else:
            col_type, col_num = st.columns(2)
            with col_type:
                edit_type = st.selectbox(
                    'Selecione o tipo de solicitação', 
                    ['Compras', 'Consumo'], 
                    key='edit_request_type'
                )
            
            options = df_purchase['request_number'].tolist() if edit_type == 'Compras' else df_consumption['request_number'].tolist()
            
            with col_num:
                if not options:
                    st.selectbox('Número da Solicitação', ['Nenhuma solicitação deste tipo'], disabled=True, key='slb_request_number_blocked')
                    selected_edit = None
                else:
                    selected_edit = st.selectbox('Número da Solicitação', options, key='slb_request_number')
            
            if selected_edit:
                req_data = get_request(selected_edit, edit_type)
                if req_data:
                    with st.form(f'form_edit_{selected_edit}'):
                        st.markdown(f'**Solicitação: {selected_edit}**')
                        
                        if edit_type == 'Consumo':
                            val = st.number_input('Valor Geral (R$)', value=float(req_data.get('requested_value') or 0.0), step=0.01)
                            rp = st.text_input('Ata RP', value=req_data.get('price_registration') or '')
                            s_date = st.text_input('Vigência Inicial (YYYY-MM-DD)', value=req_data.get('start_date') or '')
                            e_date = st.text_input('Vigência Final (YYYY-MM-DD)', value=req_data.get('end_date') or '')
                            req_unit = st.text_input('Unidade Solicitante', value=req_data.get('requesting_unit') or '')
                            fin_dep = st.text_input('Órgão Financeiro', value=req_data.get('financial_department') or '')
                            notes = st.text_area('Observação', value=req_data.get('notes') or '')
                            supp_name = st.text_input('Fornecedor', value=req_data.get('supplier_name') or '')
                            supp_cnpj = st.text_input('CNPJ', value=req_data.get('supplier_cnpj') or '')
                            
                            submitted = st.form_submit_button('Salvar Alterações')
                            if submitted:
                                new_data = {
                                    'requested_value': val,
                                    'price_registration': rp,
                                    'start_date': s_date,
                                    'end_date': e_date,
                                    'requesting_unit': req_unit,
                                    'financial_department': fin_dep,
                                    'notes': notes,
                                    'supplier_name': supp_name,
                                    'supplier_cnpj': supp_cnpj
                                }
                                if update_request(selected_edit, edit_type, new_data):
                                    st.success('Dados atualizados com sucesso!')
                                    st.rerun()
                                    
                        else:
                            val = st.number_input('Total (R$)', value=float(req_data.get('requested_value') or 0.0), step=0.01)
                            i_date = st.text_input('Data de Emissão (YYYY-MM-DD)', value=req_data.get('issue_date') or '')
                            obj = st.text_area('Objeto', value=req_data.get('object') or '')
                            notes = st.text_area('Observação', value=req_data.get('notes') or '')
                            req_unit = st.text_input('Unidade Solicitante', value=req_data.get('requesting_unit') or '')
                            fin_dep = st.text_input('Órgão Financeiro', value=req_data.get('financial_department') or '')
                            act = st.text_input('Ação', value=req_data.get('activity') or '')
                            manager = st.text_input('Gestor Indicado', value=req_data.get('designed_manager') or '')
                            leg = st.text_input('Legislação / Convênio / Contrato', value=req_data.get('legislation') or '')
                            prog = st.text_input('Programa', value=req_data.get('program') or '')
                            
                            submitted = st.form_submit_button('Salvar Alterações')
                            if submitted:
                                new_data = {
                                    'requested_value': val,
                                    'issue_date': i_date,
                                    'object': obj,
                                    'notes': notes,
                                    'requesting_unit': req_unit,
                                    'financial_department': fin_dep,
                                    'activity': act,
                                    'designed_manager': manager,
                                    'legislation': leg,
                                    'program': prog
                                }
                                if update_request(selected_edit, edit_type, new_data):
                                    st.success('Dados atualizados com sucesso!')
                                    st.rerun()

    st.subheader('Documentos Processados')
    tab_consumption, tab_purchase = st.tabs(['Solicitações de Consumo', 'Solicitações de Compras'])
    
    with tab_consumption:
        if not df_consumption.empty:
            st.dataframe(df_consumption, use_container_width=True, hide_index=True)
        else:
            st.info('Nenhuma Solicitação de Consumo cadastrada.')
            
    with tab_purchase:
        if not df_purchase.empty:
            st.dataframe(df_purchase, use_container_width=True, hide_index=True)
        else:
            st.info('Nenhuma Solicitação de Compras cadastrada.')