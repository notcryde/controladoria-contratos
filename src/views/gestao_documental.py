import streamlit as st

from src.utils.constants import (
    SOLIC_CONS_HEADERS, SOLIC_COMP_HEADERS, EMPENHOS_HEADERS, AF_HEADERS, NOTAS_FISCAIS_HEADERS,
    PAGE_HEADERS, TABS_TITLES, TIPOS_DOCS
)

from src.utils.load_dataframe import load_dataframe
from src.utils.render_table import render_table
from src.core.database import load_data

st.header(PAGE_HEADERS[1])

tabs = st.tabs(TABS_TITLES)

for tab, title in zip(tabs, TABS_TITLES):
    with tab:
        st.subheader(title)

        if title == TABS_TITLES[0]:
            with st.expander(label=TIPOS_DOCS[0], expanded=True):
                dataframe_solicitacoes_consumo = load_dataframe(SOLIC_CONS_HEADERS, 'solicitacoes_consumo', load_data)
                dataframe = render_table(dataframe_solicitacoes_consumo, SOLIC_CONS_HEADERS)
            
            with st.expander(label=TIPOS_DOCS[1], expanded=True):
                dataframe_solicitacoes_compras = load_dataframe(SOLIC_COMP_HEADERS, 'solicitacoes_compras', load_data)
                dataframe = render_table(dataframe_solicitacoes_compras, SOLIC_COMP_HEADERS)

        if title == TABS_TITLES[1]:
            dataframe_empenhos = load_dataframe(EMPENHOS_HEADERS, 'empenhos', load_data)
            dataframe = render_table(dataframe_empenhos, EMPENHOS_HEADERS)

        if title == TABS_TITLES[2]:
            dataframe_autorizacoes = load_dataframe(AF_HEADERS, 'autorizacoes', load_data)
            dataframe = render_table(dataframe_autorizacoes, AF_HEADERS)

        if title == TABS_TITLES[3]:
            dataframe_notas_fiscais = load_dataframe(NOTAS_FISCAIS_HEADERS, 'notas_fiscais', load_data)
            dataframe = render_table(dataframe_notas_fiscais, NOTAS_FISCAIS_HEADERS)
