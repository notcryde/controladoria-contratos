import streamlit as st

from utils.pdf_extractor import extract_text_from_pdf, extract_data, extract_items
from utils.regex_patterns import INVOICES, INVOICE_ITEMS
from utils.headers import INVOICES_HEADERS, INVOICE_ITEMS_HEADERS
from utils.formatters import format_currency

import core.invoices as inv
import core.invoice_items as item

def _expander_new_invoice():
    with st.expander('Processar Novas Notas Fiscais', expanded=False):
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
                        
                        invoice_data = extract_data(pdf_text, INVOICES)
                        items_data = extract_items(pdf_text, INVOICE_ITEMS)
                        inv_number = invoice_data.get('invoice_number', uploaded_file.name)
                        
                        if not items_data:
                            st.warning(f'NF {inv_number}: A captura detectou a NF, mas os itens formatados corretamente não foram identificados.')
                        
                        if inv.insert(invoice_data, items_data):
                            st.success(f'NF {inv_number}: A nota e os itens vinculados foram processados com sucesso!')
                    
                    st.rerun()
            else:
                st.warning('Selecione pelo menos um arquivo PDF antes de processar.')

def _expander_update_invoice():
        df_invoices = inv.get_all()
        has_data = not df_invoices.empty

        with st.expander('Atualizar NF', expanded=False):
            if not has_data:
                st.info('As notas fiscais não estão cadastradas no sistema.')
            else:
                options = df_invoices['invoice_number'].tolist()
                selected_edit = st.selectbox('Número da Nota Fiscal', options, key='edit_inv_num')
                
                if selected_edit:
                    invoice_data = inv.get_by_id(selected_edit)
                    if invoice_data:
                        with st.form(f'form_update_invoice'):                            
                            issue_date = st.text_input('Data de Emissão (YYYY-MM-DD)', value=invoice_data.get('issue_date') or '')
                            
                            submit_button = st.form_submit_button('Salvar Alterações', key='btn_submit_invoice')
                            if submit_button:
                                data = {
                                    'issue_date': issue_date,
                                }
                                if inv.update(selected_edit, data):
                                    st.success('Os dados foram atualizados com sucesso!')
                                    st.rerun()

def _expander_update_item():
    df_invoices = inv.get_all()
    has_data = not df_invoices.empty
    
    with st.expander('Atualizar Item', expanded=False):
        if not has_data:
            st.info('As notas fiscais não estão cadastradas no sistema.')
        else:
            options = df_invoices['invoice_number'].tolist()
            invoice_number_item = st.selectbox('Número da Nota Fiscal', options, key='edit_item_inv_num')
            
            if invoice_number_item:
                items = item.get_by_invoice_number(invoice_number_item)
                if not items:
                    st.info('Os itens vinculados a esta Nota Fiscal não existem.')
                else:
                    material_code = st.selectbox(
                        'Código Material', 
                        items, 
                        format_func=lambda x: x['material_code'],
                        key='slb_item_material_code'
                    )
                    
                    if material_code:
                        item_id = material_code['id']
                        item_data = item.get_by_id(item_id)
                        
                        if item_data:
                            with st.form(key='form_update_item'):                                
                                description = st.text_area('Descrição', value=item_data.get('description') or '')
                                quantity = st.number_input('Quantidade', value=float(item_data.get('quantity') or 0.0), step=0.01)
                                unitary_value = st.number_input('Valor Unitário (R$)', value=float(item_data.get('unitary_value') or 0.0), step=0.01)
                                
                                submit_button_item = st.form_submit_button('Salvar Alterações', key='btn_submit_item_invoice')
                                if submit_button_item:
                                    data = {
                                        'description': description,
                                        'quantity': quantity,
                                        'unitary_value': unitary_value
                                    }
                                    if item.update(item_id, data):
                                        st.success('O item foi atualizado com sucesso!')
                                        st.rerun()

def _dataframe_section():
    df_invoices = inv.get_all()
    has_data = not df_invoices.empty

    st.subheader('Notas Fiscais Processadas')
    
    tab1, tab2 = st.tabs(['Notas Fiscais', 'Itens de NF'])
    
    with tab1:
        if has_data:
            df_display = df_invoices.rename(columns=INVOICES_HEADERS)
            st.dataframe(df_display, width='stretch', hide_index=True)
        else:
            st.info('A Nota Fiscal não está cadastrada.')
            
    with tab2:
        if has_data:
            invoices = df_invoices['invoice_number'].tolist()
            invoice_number = st.selectbox(
                'Selecione o número da Nota Fiscal', 
                invoices,
                key='slb_invoice_number'
            )
            
            if invoice_number:
                df_items = item.get_all(invoice_number)
                if not df_items.empty:
                    df_display = df_items.copy()
                    
                    df_display['executed_value'] = df_display['quantity'] * df_display['unitary_value']
                    
                    currency_cols = ['unitary_value', 'executed_value']
                    for col in currency_cols:
                        df_display[col] = df_display[col].apply(format_currency)
                        
                    df_display = df_display.rename(columns=INVOICE_ITEMS_HEADERS)
                    st.dataframe(df_display, width='stretch', hide_index=True)
                else:
                    st.info('Nenhum item foi encontrado para esta Nota Fiscal.')
        else:
            st.info('As Notas Fiscais não estão cadastradas para exibir itens.')

def render():
    st.header('Gestão de Notas Fiscais')
    
    _expander_new_invoice()
    _expander_update_invoice()
    _expander_update_item()
    _dataframe_section()
    
    