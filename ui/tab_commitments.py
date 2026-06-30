import streamlit as st

from utils.pdf_extractor import extract_text_from_pdf, extract_data
from utils.regex_patterns import COMMITMENTS
from utils.headers import COMMITMENTS_HEADERS
from utils.formatters import format_currency

import core.commitments as comm

def _expander_new_commitment():
    with st.expander('Criar Empenho', expanded=True):
        left_column, right_column = st.columns(2)
        
        with left_column:
            req_type = st.selectbox(
                'Selecione o tipo de solicitação', 
                ['Compras', 'Consumo'],
                key='slb_req_type'
            )
            
            available_requests = comm.get_available_requests(req_type)
            
            if available_requests:
                request_number = st.selectbox(
                    'Selecione o número de solicitação', 
                    available_requests,
                    key='slb_req_number'
                )
                is_blocked = False
            else:
                st.selectbox(
                    'Selecione o número de solicitação', 
                    ['Não há solicitações cadastradas para este tipo'], 
                    disabled=True
                )
                is_blocked = True
                
        with right_column:
            pdf = st.file_uploader(
                'Faça o upload do empenho (PDF)', 
                type=['pdf'],
                key='commit_upload',
                disabled=is_blocked
            )
            
        if st.button('Processar', type='primary', disabled=is_blocked, key='btn_process_commitment_blocked'):
            if pdf is not None:
                with st.spinner('Extraindo dados do empenho...'):
                    pdf_text = extract_text_from_pdf(pdf)
                    
                    if not pdf_text.strip():
                        st.error('Não foi possível extrair texto do documento.')
                    else:
                        extracted_data = extract_data(pdf_text, COMMITMENTS)
                        
                        if comm.insert(extracted_data, request_number):
                            st.success(f'Empenho processado e vinculado à solicitação {request_number} com sucesso!')
                            st.rerun()
            else:
                st.warning('Selecione um arquivo PDF antes de processar.')

def _expander_update_commitment():
    df_commitments = comm.get_all()
    has_data = not df_commitments.empty

    with st.expander('Editar Dados', expanded=False):
        if not has_data:
            st.info('Não há empenhos cadastrados no sistema.')
        else:
            options = df_commitments['commitment_number'].tolist()
            selected_edit = st.selectbox('Número do Empenho', options, key='slb_upd_commitment_number')
            
            if selected_edit:
                commit_data = comm.get_by_id(selected_edit)
                if commit_data:
                    with st.form(f'form_update_commitment'):
                        st.markdown(f'**Empenho:** {selected_edit}')
                        
                        commited_value = st.number_input('Valor do Empenho (R$)', value=float(commit_data.get('commited_value') or 0.0), step=0.01)
                        process_number = st.text_input('Processo Nº', value=commit_data.get('process_number') or '')
                        source = st.text_input('Fonte de Recurso', value=commit_data.get('source') or '')
                        supplier_name = st.text_input('Credor (Nome)', value=commit_data.get('supplier_name') or '')
                        supplier_cnpj = st.text_input('CPF/CNPJ', value=commit_data.get('supplier_cnpj') or '')
                        supplier_phone = st.text_input('Telefone', value=commit_data.get('supplier_phone') or '')
                        supplier_email = st.text_input('E-mail', value=commit_data.get('supplier_email') or '')
                        
                        submitted = st.form_submit_button('Salvar Alterações', key='btn_submit_commitment')
                        if submitted:
                            new_data = {
                                'commited_value': commited_value,
                                'process_number': process_number,
                                'source': source,
                                'supplier_name': supplier_name,
                                'supplier_cnpj': supplier_cnpj,
                                'supplier_phone': supplier_phone,
                                'supplier_email': supplier_email
                            }
                            if comm.update(selected_edit, new_data):
                                st.success('Dados atualizados com sucesso!')
                                st.rerun()

def _dataframe_section():
    st.subheader('Empenhos Processados')

    df_commitments = comm.get_all()

    if not df_commitments.empty:
        df_display = df_commitments.copy()
        df_display['commited_value'] = df_display['commited_value'].apply(format_currency)
        df_display = df_display.rename(columns=COMMITMENTS_HEADERS)
        st.dataframe(df_display, width='stretch', hide_index=True)
    else:
        st.info('Nenhum Empenho cadastrado.')

def render():
    st.header('Gestão de Empenhos')
    
    _expander_new_commitment()
    _expander_update_commitment()
    _dataframe_section()