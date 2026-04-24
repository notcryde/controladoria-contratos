import streamlit as st
import pandas as pd

from src.utils.constants import (
    SOLIC_CONS_HEADERS, SOLIC_COMP_HEADERS, EMPENHOS_HEADERS, AF_HEADERS, NOTAS_FISCAIS_HEADERS,
    PAGE_HEADERS, TABS_TITLES, TIPOS_DOCS
)

from src.utils.load_dataframe import load_dataframe
from src.utils.render_table import render_table
from src.utils.database import load_data, load_items_notas_fiscais

if 'modal_notas_fiscais_id' not in st.session_state:
    st.session_state.modal_notas_fiscais_id = None
if 'aggrid_reset_key' not in st.session_state:
    st.session_state.aggrid_reset_key = 0

st.header(PAGE_HEADERS[1])

st.markdown('''
    <style>
    div[data-testid='stDialog'] div[role='dialog'] {
        max-width: 75vw;
    }
    </style>
    ''', 
    unsafe_allow_html=True
)

@st.dialog('Itens da Nota Fiscal', width='large')
def modal_notas_fiscais(notas_fiscais_id):
    st.write(f'Detalhamento da NF: **{notas_fiscais_id}**')
    dataframe_items = load_items_notas_fiscais(notas_fiscais_id)
    if not dataframe_items.empty:
        st.dataframe(dataframe_items, width='stretch', hide_index=True)
    else:
        st.warning('Nenhum item encontrado.')

if st.session_state.modal_notas_fiscais_id:
    modal_notas_fiscais(st.session_state.modal_notas_fiscais_id)
    st.session_state.modal_notas_fiscais_id = None

tabs = st.tabs(TABS_TITLES)

for tab, title in zip(tabs, TABS_TITLES):
    with tab:
        st.subheader(title)

        if title == TABS_TITLES[0]:
            with st.expander(label=TIPOS_DOCS[0], expanded=True):
                dataframe_consumo = load_dataframe(SOLIC_CONS_HEADERS, 'solicitacoes_consumo', load_data)
                render_table(dataframe_consumo, SOLIC_CONS_HEADERS, key='grid_consumo', export_name='solicitacoes_consumo')
            with st.expander(label=TIPOS_DOCS[1], expanded=True):
                dataframe_compras = load_dataframe(SOLIC_COMP_HEADERS, 'solicitacoes_compras', load_data)
                render_table(dataframe_compras, SOLIC_COMP_HEADERS, key='grid_compras', export_name='solicitacoes_compras')

        elif title == TABS_TITLES[1]:
            dataframe_empenhos = load_dataframe(EMPENHOS_HEADERS, 'empenhos', load_data)
            render_table(dataframe_empenhos, EMPENHOS_HEADERS, key='grid_empenhos', export_name='empenhos')

        elif title == TABS_TITLES[2]:
            dataframe_autorizacoes = load_dataframe(AF_HEADERS, 'autorizacoes', load_data)
            render_table(dataframe_autorizacoes, AF_HEADERS, key='grid_af', export_name='autorizacoes_fornecimento')

        elif title == TABS_TITLES[3]:
            dataframe_notas_fiscais = load_dataframe(NOTAS_FISCAIS_HEADERS, 'notas_fiscais', load_data)
            
            _, selected_rows = render_table(
                dataframe_notas_fiscais, 
                NOTAS_FISCAIS_HEADERS, 
                enable_selection=True, 
                key=f'grid_notas_fiscais_{st.session_state.aggrid_reset_key}',
                export_name='notas_fiscais'
            )
            
            if selected_rows is not None and len(selected_rows) > 0:
                if isinstance(selected_rows, pd.DataFrame):
                    notas_fiscais_id = selected_rows.iloc[0]['Nº NF']
                else:
                    notas_fiscais_id = selected_rows[0]['Nº NF']
                
                st.session_state.modal_notas_fiscais_id = notas_fiscais_id
                st.session_state.aggrid_reset_key += 1
                st.rerun()