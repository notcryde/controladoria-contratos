import streamlit as st
import pandas as pd
import sqlite3
import logging
from database.connection import get_connection
from core.pdf_extractor import extract_text_from_pdf, extract_data
from core.regex_patterns import COMMITMENTS

from core.formatters import parse_currency


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

def insert_commitment(extracted_data: dict, selected_request: str) -> bool:
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

def load_commitments() -> pd.DataFrame:
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

def get_commitment(commitment_number: str) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM commitments WHERE commitment_number = ?', (commitment_number,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    finally:
        conn.close()

def update_commitment(commitment_number: str, data: dict) -> bool:
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

def render():
    st.header('Gestão de Empenhos')
    
    df_commitments = load_commitments()
    has_data = not df_commitments.empty

    with st.expander('Processar Novo Empenho', expanded=True):
        col1, col2 = st.columns(2)
        
        with col1:
            req_type = st.selectbox(
                'Selecione o tipo de solicitação', 
                ['Compras', 'Consumo'],
                key='commit_req_type'
            )
            
            available_requests = get_available_requests(req_type)
            
            if available_requests:
                selected_request = st.selectbox(
                    'Selecione o número de solicitação', 
                    available_requests
                )
                is_blocked = False
            else:
                st.selectbox(
                    'Selecione o número de solicitação', 
                    ['Não há solicitações cadastradas para este tipo'], 
                    disabled=True
                )
                is_blocked = True
                
        with col2:
            uploaded_file = st.file_uploader(
                'Faça o upload do empenho (PDF)', 
                type=['pdf'],
                key='commit_upload',
                disabled=is_blocked
            )
            
        if st.button('Processar', type='primary', disabled=is_blocked, key='btn_process_commitment_blocked'):
            if uploaded_file is not None:
                with st.spinner('Extraindo dados do empenho...'):
                    pdf_text = extract_text_from_pdf(uploaded_file)
                    
                    if not pdf_text.strip():
                        st.error('Não foi possível extrair texto do documento.')
                    else:
                        extracted_data = extract_data(pdf_text, COMMITMENTS)
                        
                        if insert_commitment(extracted_data, selected_request):
                            st.success(f'Empenho processado e vinculado à solicitação {selected_request} com sucesso!')
                            st.rerun()
            else:
                st.warning('Selecione um arquivo PDF antes de processar.')

    with st.expander('Editar Dados', expanded=False):
        if not has_data:
            st.info('Não há empenhos cadastrados no sistema.')
        else:
            options = df_commitments['commitment_number'].tolist()
            selected_edit = st.selectbox('Número do Empenho', options, key='edit_commit_num')
            
            if selected_edit:
                commit_data = get_commitment(selected_edit)
                if commit_data:
                    with st.form(f'form_edit_{selected_edit}'):
                        st.markdown(f'**Editando Empenho: {selected_edit}**')
                        
                        val = st.number_input('Valor do Empenho (R$)', value=float(commit_data.get('commited_value') or 0.0), step=0.01)
                        proc = st.text_input('Processo Nº', value=commit_data.get('process_number') or '')
                        src = st.text_input('Fonte de Recurso', value=commit_data.get('source') or '')
                        s_name = st.text_input('Credor (Nome)', value=commit_data.get('supplier_name') or '')
                        s_cnpj = st.text_input('CPF/CNPJ', value=commit_data.get('supplier_cnpj') or '')
                        s_phone = st.text_input('Telefone', value=commit_data.get('supplier_phone') or '')
                        s_email = st.text_input('E-mail', value=commit_data.get('supplier_email') or '')
                        
                        submitted = st.form_submit_button('Salvar Alterações', key='btn_submit_commitment')
                        if submitted:
                            new_data = {
                                'commited_value': val,
                                'process_number': proc,
                                'source': src,
                                'supplier_name': s_name,
                                'supplier_cnpj': s_cnpj,
                                'supplier_phone': s_phone,
                                'supplier_email': s_email
                            }
                            if update_commitment(selected_edit, new_data):
                                st.success('Dados atualizados com sucesso!')
                                st.rerun()

    st.markdown('---')
    
    st.subheader('Empenhos Processados')
    
    if not df_commitments.empty:
        st.dataframe(df_commitments, use_container_width=True, hide_index=True)
    else:
        st.info('Nenhum Empenho cadastrado.')