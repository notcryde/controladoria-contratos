import streamlit as st
import pandas as pd

from src.utils.constants import (
    SOLIC_CONS_HEADERS, SOLIC_COMP_HEADERS, EMPENHOS_HEADERS, AF_HEADERS, NOTAS_FISCAIS_HEADERS,
    PAGE_HEADERS, TABS_TITLES, TIPOS_DOCS
)

from src.utils.load_dataframe import load_dataframe
from src.utils.render_table import render_table
from src.utils.database import load_data, load_nf_items

# Inicializa estados para controle da modal e reset da tabela
if "nf_modal_id" not in st.session_state:
    st.session_state.nf_modal_id = None
if "aggrid_reset_key" not in st.session_state:
    st.session_state.aggrid_reset_key = 0

st.header(PAGE_HEADERS[1])

st.markdown("""
    <style>
    div[data-testid="stDialog"] div[role="dialog"] {
        max-width: 75vw;
    }
    </style>
    """, unsafe_allow_html=True)

@st.dialog("Itens da Nota Fiscal", width="large")
def show_nf_items_modal(nf_id):
    st.write(f"Detalhamento da NF: **{nf_id}**")
    df_items = load_nf_items(nf_id)
    if not df_items.empty:
        st.dataframe(df_items, width='stretch', hide_index=True)
    else:
        st.warning("Nenhum item encontrado.")

# Gatilho para abrir a modal após o rerun de limpeza
if st.session_state.nf_modal_id:
    show_nf_items_modal(st.session_state.nf_modal_id)
    st.session_state.nf_modal_id = None

tabs = st.tabs(TABS_TITLES)

for tab, title in zip(tabs, TABS_TITLES):
    with tab:
        st.subheader(title)

        if title == TABS_TITLES[0]:
            with st.expander(label=TIPOS_DOCS[0], expanded=True):
                df_cons = load_dataframe(SOLIC_CONS_HEADERS, 'solicitacoes_consumo', load_data)
                render_table(df_cons, SOLIC_CONS_HEADERS, key="grid_cons")
            with st.expander(label=TIPOS_DOCS[1], expanded=True):
                df_comp = load_dataframe(SOLIC_COMP_HEADERS, 'solicitacoes_compras', load_data)
                render_table(df_comp, SOLIC_COMP_HEADERS, key="grid_comp")

        elif title == TABS_TITLES[1]:
            df_emp = load_dataframe(EMPENHOS_HEADERS, 'empenhos', load_data)
            render_table(df_emp, EMPENHOS_HEADERS, key="grid_emp")

        elif title == TABS_TITLES[2]:
            df_af = load_dataframe(AF_HEADERS, 'autorizacoes', load_data)
            render_table(df_af, AF_HEADERS, key="grid_af")

        elif title == TABS_TITLES[3]:
            df_nf = load_dataframe(NOTAS_FISCAIS_HEADERS, 'notas_fiscais', load_data)
            
            _, selected_rows = render_table(
                df_nf, 
                NOTAS_FISCAIS_HEADERS, 
                enable_selection=True, 
                key=f"grid_nf_{st.session_state.aggrid_reset_key}"
            )
            
            if selected_rows is not None and len(selected_rows) > 0:
                if isinstance(selected_rows, pd.DataFrame):
                    nf_id = selected_rows.iloc[0]['Nº NF']
                else:
                    nf_id = selected_rows[0]['Nº NF']
                
                st.session_state.nf_modal_id = nf_id
                st.session_state.aggrid_reset_key += 1
                st.rerun()