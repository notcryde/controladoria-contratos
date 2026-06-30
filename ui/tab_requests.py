import streamlit as st

from utils.pdf_extractor import extract_text_from_pdf, extract_data
from utils.regex_patterns import CONSUMPTION_REQUESTS, PURCHASE_REQUESTS
from utils.headers import CONSUMPTION_REQUESTS_HEADERS, PURCHASE_REQUESTS_HEADERS
from utils.formatters import format_currency

import core.requests as req

def _expander_new_request():
    with st.expander('Criar Solicitação', expanded=True):
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
                        
                        if req.insert(request_type, extracted_data):
                            st.success(f'Solicitação de {request_type} processada e salva com sucesso!')
                            st.rerun()
            else:
                st.warning('Selecione um arquivo PDF antes de processar.')

def _expander_update_request():
    df_consumption = req.get_all('consumption_requests')
    df_purchase = req.get_all('purchase_requests')
    has_data = not df_consumption.empty or not df_purchase.empty
    
    with st.expander('Editar Solicitação', expanded=False):
        if not has_data:
            st.info('Não há solicitações cadastradas no sistema.')
        else:
            left_column, right_column = st.columns(2)

            with left_column:
                request_type = st.selectbox(
                    'Selecione o tipo de solicitação', 
                    ['Compras', 'Consumo'], 
                    key='slb_update_req_type'
                )
            
            
            with right_column:
                options = df_purchase['request_number'].tolist() if request_type == 'Compras' else df_consumption['request_number'].tolist()
                if not options:
                    st.selectbox('Número da Solicitação', ['Nenhuma solicitação deste tipo'], disabled=True, key='slb_req_number_blocked')
                    request_number = None
                else:
                    request_number = st.selectbox('Número da Solicitação', options, key='slb_req_number')
            
            if request_number:
                request_data = req.get_by_id(request_number, request_type)
                if request_data:
                    with st.form(f'form_update_request'):
                        st.markdown(f'**Solicitação:** {request_number}')
                        
                        if request_type == 'Consumo':
                            requested_value = st.number_input('Valor Geral (R$)', value=float(request_data.get('requested_value') or 0.0), step=0.01)
                            price_registration = st.text_input('Ata RP', value=request_data.get('price_registration') or '')
                            start_date = st.text_input('Vigência Inicial (YYYY-MM-DD)', value=request_data.get('start_date') or '')
                            end_date = st.text_input('Vigência Final (YYYY-MM-DD)', value=request_data.get('end_date') or '')
                            requesting_unit = st.text_input('Unidade Solicitante', value=request_data.get('requesting_unit') or '')
                            financial_department = st.text_input('Órgão Financeiro', value=request_data.get('financial_department') or '')
                            notes = st.text_area('Observação', value=request_data.get('notes') or '')
                            supplier_name = st.text_input('Fornecedor', value=request_data.get('supplier_name') or '')
                            supplier_cnpj = st.text_input('CNPJ', value=request_data.get('supplier_cnpj') or '')
                            
                            submit_button = st.form_submit_button('Salvar Alterações', type='primary', key='btn_update_request')
                            if submit_button:
                                data = {
                                    'requested_value': requested_value,
                                    'price_registration': price_registration,
                                    'start_date': start_date,
                                    'end_date': end_date,
                                    'requesting_unit': requesting_unit,
                                    'financial_department': financial_department,
                                    'notes': notes,
                                    'supplier_name': supplier_name,
                                    'supplier_cnpj': supplier_cnpj
                                }
                                if req.update(request_number, request_type, data):
                                    st.success('Dados atualizados com sucesso!')
                                    st.rerun()
                                    
                        else:
                            requested_value = st.number_input('Total (R$)', value=float(request_data.get('requested_value') or 0.0), step=0.01)
                            issue_date = st.text_input('Data de Emissão (YYYY-MM-DD)', value=request_data.get('issue_date') or '')
                            object = st.text_area('Objeto', value=request_data.get('object') or '')
                            notes = st.text_area('Observação', value=request_data.get('notes') or '')
                            requesting_unit = st.text_input('Unidade Solicitante', value=request_data.get('requesting_unit') or '')
                            financial_department = st.text_input('Órgão Financeiro', value=request_data.get('financial_department') or '')
                            activity = st.text_input('Ação', value=request_data.get('activity') or '')
                            designed_manager = st.text_input('Gestor Indicado', value=request_data.get('designed_manager') or '')
                            legislation = st.text_input('Legislação / Convênio / Contrato', value=request_data.get('legislation') or '')
                            program = st.text_input('Programa', value=request_data.get('program') or '')
                            
                            submit_button = st.form_submit_button('Salvar Alterações')
                            if submit_button:
                                data = {
                                    'requested_value': requested_value,
                                    'issue_date': issue_date,
                                    'object': object,
                                    'notes': notes,
                                    'requesting_unit': requesting_unit,
                                    'financial_department': financial_department,
                                    'activity': activity,
                                    'designed_manager': designed_manager,
                                    'legislation': legislation,
                                    'program': program
                                }

                                if req.update(request_number, request_type, data):
                                    st.success('Dados atualizados com sucesso!')
                                    st.rerun()

def _dataframe_section():
    tab_consumption, tab_purchase = st.tabs(['Solicitações de Consumo', 'Solicitações de Compras'])
    
    df_consumption = req.get_all('consumption_requests')
    df_purchase = req.get_all('purchase_requests')

    with tab_consumption:
        if not df_consumption.empty:
            df_display = df_consumption.copy()
            df_display['requested_value'] = df_display['requested_value'].apply(format_currency)
            df_display = df_display.rename(columns=CONSUMPTION_REQUESTS_HEADERS)
            st.dataframe(df_display, width='stretch', hide_index=True)
        else:
            st.info('Nenhuma Solicitação de Consumo cadastrada.')
            
    with tab_purchase:
        if not df_purchase.empty:
            df_display = df_purchase.copy()
            df_display['requested_value'] = df_display['requested_value'].apply(format_currency)
            df_display = df_display.rename(columns=PURCHASE_REQUESTS_HEADERS)
            st.dataframe(df_display, width='stretch', hide_index=True)
        else:
            st.info('Nenhuma Solicitação de Compras cadastrada.')

def render():
    st.header('Gestão de Solicitações')
    
    df_consumption = req.get_all('consumption_requests')
    df_purchase = req.get_all('purchase_requests')
    has_data = not df_consumption.empty or not df_purchase.empty

    _expander_new_request()
    _expander_update_request()
    
    st.subheader('Documentos Processados')

    _dataframe_section()