import streamlit as st

from utils.pdf_extractor import extract_text_from_pdf, extract_data, extract_items
from utils.regex_patterns import AUTHORIZATIONS, AUTHORIZATION_ITEMS
from utils.headers import AUTHORIZATIONS_HEADERS, AUTHORIZATION_ITEMS_HEADERS
from utils.formatters import format_currency

import core.authorizations as auth
import core.authorization_items as item

def _expander_new_authorization():
    with st.expander('Criar AF', expanded=False, key='exp_new_auth'):
        right_column, left_column = st.columns(2)
        
        with right_column:
            start_date = st.date_input(label='Selecione a data inicial:', format='DD/MM/YYYY', key='dti_start_date')
            end_date = st.date_input(label='Selecione a data final:', format='DD/MM/YYYY', key='dti_end_date')
            
        with left_column:
            pdf = st.file_uploader(
                label='Faça o upload aqui:', 
                type=['pdf'],
                key='slb_pdf_upload'
            )
            
        if st.button('Processar', type='primary', key='btn_process_auth'):
            if pdf is not None:
                if start_date > end_date:
                    st.error('A data inicial não pode ser posterior à data final.')
                else:
                    with st.spinner('Extraindo dados da autorização...'):
                        raw_text = extract_text_from_pdf(pdf)
                        
                        if not raw_text.strip():
                            st.error('O texto do documento não foi extraído.')
                        else:
                            auth_data = extract_data(raw_text, AUTHORIZATIONS)
                            items_data = extract_items(raw_text, AUTHORIZATION_ITEMS)
                            
                            if not items_data:
                                st.warning('A captura detectou a autorização, mas os itens não foram identificados.')
                            
                            if auth.insert(auth_data, items_data, start_date, end_date):
                                st.success('A autorização e os itens vinculados foram processados com sucesso!')
                                st.rerun()
            else:
                st.warning('Selecione um arquivo PDF antes de processar.')

def _expander_update_authorization():
    df_authorizations = auth.get_all()
    has_data = not df_authorizations.empty

    with st.expander('Atualizar AF', expanded=False, key='exp_update_auth'):
        if not has_data:
            st.info('As autorizações não estão cadastradas no sistema.')
        else:
            options = df_authorizations['authorization_number'].tolist()
            authorization_number = st.selectbox('Número da Autorização', options, key='slb_update_auth_number')
            
            if authorization_number:
                auth_data = auth.get_by_id(authorization_number)
                if auth_data:
                    with st.form(f'form_update_auth'):
                        st.markdown(f'**Nº AF:** {authorization_number}')
                        
                        process_number = st.text_input('Nº Processo', value=auth_data.get('process_number') or '')
                        modality = st.text_input('Modalidade', value=auth_data.get('modality') or '')
                        contract = st.text_input('Contrato / Ano', value=auth_data.get('contract') or '')
                        notes = st.text_area('Observações', value=auth_data.get('notes') or '')
                        budget_sheet = st.text_input('Ficha', value=auth_data.get('budget_sheet') or '')
                        budget_allocation = st.text_input('Dotação', value=auth_data.get('budget_allocation') or '')
                        start_date = st.text_input('Data Inicial (YYYY-MM-DD)', value=auth_data.get('start_date') or '')
                        end_date = st.text_input('Data Final (YYYY-MM-DD)', value=auth_data.get('end_date') or '')
                        
                        submit_button = st.form_submit_button(label='Salvar Alterações', type='secondary', width='stretch', key='btn_update_auth')
                        if submit_button:
                            data = {
                                'process_number': process_number,
                                'modality': modality,
                                'contract': contract,
                                'notes': notes,
                                'budget_sheet': budget_sheet,
                                'budget_allocation': budget_allocation,
                                'start_date': start_date,
                                'end_date': end_date
                            }

                            if auth.update(authorization_number, data):
                                st.success('Os dados foram atualizados com sucesso!')
                                st.rerun()

def _expander_update_item():
    df_authorizations = auth.get_all()
    has_data = not df_authorizations.empty

    with st.expander('Atualizar Item', expanded=False):
        if not has_data:
            st.info('Não há AFs cadastradas no sistema.')
        else:
            options = df_authorizations['authorization_number'].tolist()
            auth_number = st.selectbox('Número da AF', options, key='slb_upd_item_auth_number')
            
            if auth_number:
                items_for_select = item.get_by_auth_number(auth_number)
                if not items_for_select:
                    st.info('Os itens vinculados a esta Autorização não existem.')
                else:
                    material_code = st.selectbox(
                        label='Código Material', 
                        options=items_for_select, 
                        format_func=lambda x: x['material_code'],
                        key='update_item'
                    )
                    
                    if material_code:
                        item_id = material_code['id']
                        item_data = item.get_by_id(item_id)
                        
                        if item_data:
                            with st.form(f'form_update_auth_item'):
                                st.markdown(f'**Item:** {item_data["material_code"]}')
                                
                                description = st.text_area(label='Descrição', value=item_data.get('description') or '')
                                quantity = st.number_input(label='Quantidade', value=float(item_data.get('quantity') or 0.0), step=0.01)
                                unitary_value = st.number_input(label='Valor Unitário (R$)', value=float(item_data.get('unitary_value') or 0.0), step=0.01)
                                
                                submitted_item = st.form_submit_button('Salvar Alterações')
                                if submitted_item:
                                    data = {
                                        'description': description,
                                        'quantity': quantity,
                                        'unitary_value': unitary_value
                                    }
                                    if item.update(item_id, data):
                                        st.success('O item foi atualizado com sucesso!')
                                        st.rerun()
    
def _dataframe_section():
    df_authorizations = auth.get_all()
    has_data = not df_authorizations.empty

    tab1, tab2 = st.tabs(['Autorizações', 'Itens de AF'])

    with tab1:
        if has_data:
            df_display = df_authorizations.rename(columns=AUTHORIZATIONS_HEADERS)
            st.dataframe(df_display, width='stretch', hide_index=True)
        else:
            st.info('A Autorização não está cadastrada.')
            
    with tab2:
        if has_data:
            authorizations = df_authorizations['authorization_number'].tolist()
            authorization_number = st.selectbox(
                'Selecione o número da AF', 
                authorizations,
                key='slb_auth_number_view'
            )
            
            if authorization_number:
                df_items = item.get_all(authorization_number)
                if not df_items.empty:
                    df_display = df_items.copy()
                    df_display['unitary_value'] = df_display['unitary_value'].apply(format_currency)
                    df_display = df_display.rename(columns=AUTHORIZATION_ITEMS_HEADERS)
                    st.dataframe(df_display, width='stretch', hide_index=True)
                else:
                    st.info('Nenhum item foi encontrado para esta Autorização.')
        else:
            st.info('As Autorizações não estão cadastradas para exibir itens.')

def render():
    st.header('Gestão de Autorizações de Fornecimento')
    
    _expander_new_authorization()
    _expander_update_authorization()
    _expander_update_item()

    st.subheader('Autorizações Processadas')

    _dataframe_section()
